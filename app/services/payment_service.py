from app.repositories import PaymentsRepo, OrdersRepo
from datetime import datetime, date, time
from typing import Any
from app.services import OrderService
from app.exceptions import PaymentFailed, UnexpectedErrorAccuerd, logger, InvalidCerdiantials, NotFoundError



class PaymentsService:
    def __init__(self, customer_id : int, db):
        self.customer_id = customer_id
        self.__payments_db = PaymentsRepo(db)
        self.__orders_db = OrdersRepo(db)
        self.__order_service = OrderService(customer_id, db)


    def __generate_transaction_id(self) -> str:
        now = datetime.now()

        letters = "TXN"
        date_time = now.strftime("%Y%m%d%H%M%S%f")
        txn_id = letters + date_time
        return txn_id

    def __make_transaction(self, order_id : str, amount : int, txn_method : str) -> object:
        try:
            order_id = str(order_id)
            amount = int(amount)
            txn_method = str(txn_method)
            new_transaction = self.__payments_db.create_transaction(
                txn_id= self.__generate_transaction_id(),
                customer_id= self.customer_id,
                order_id= order_id,
                amount= amount,
                txn_method= txn_method
            )
            if not new_transaction:
                raise UnexpectedErrorAccuerd("Unable To Create Transaction At This Moment")
            else:
                return new_transaction
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise

          
        
    def make_payment(self, order_id : str, total_amount : int, **cerdentials : dict) -> object: # need to add upi and card logic and self amount getter
        try:
            pay_options = ["COD", "UPI", "CARD"]
            order_id = str(order_id)
            order = self.__orders_db.get_order(order_id) #order id must needed to exists
            if not order:
                raise InvalidCerdiantials("Invalid Order Id")
            if order.payment != "Not Paid":
                raise InvalidCerdiantials("Already Paid")
            total_amount = int(total_amount)
            payment_method = cerdentials.get("method")
            if payment_method in pay_options:
                if payment_method == "COD":
                    update_order = self.__orders_db.update_status(order_id, "payment", "COD")
                    if not update_order:
                        delete_txn = self.__payments_db.delete_transaction(transaction.txn_id)
                        raise PaymentFailed("Payment Failed")
                    return update_order
                elif payment_method == "UPI":
                    supporitng_partners = ("@upi", "@ybl", "@api", "@apl")
                    if cerdentials.get("upi_id").endswith(supporitng_partners):
                        transaction = self.__make_transaction(order_id, total_amount, payment_method)
                        if transaction:
                            update_order = self.__orders_db.update_status(order_id, "payment", "Paid")
                            if not update_order:
                                delete_txn = self.__payments_db.delete_transaction(transaction.txn_id)
  
                                raise PaymentFailed("Payment Failed")
                            return transaction
                        else:
                            raise PaymentFailed("Payment Failed")
                    else:
                        raise InvalidCerdiantials("We are not acception this upi")

                elif payment_method == "Card":
                    if len(cerdentials.get("card_number")) != 16:
                        raise InvalidCerdiantials("Invalid Card Number")
                    if cerdentials.get("expiry_date") < date.today():
                        raise InvalidCerdiantials("Date Expired")
                    transaction = self.__make_transaction(order_id, total_amount, payment_method)
                    if transaction:
                        update_order = self.__orders_db.update_status(order_id, "payment", "Paid")
                        if not update_order:
                            delete_txn = self.__payments_db.delete_transaction(transaction.txn_id)
                            raise PaymentFailed("Payment Failed")

                        return transaction
                    else:
                        raise PaymentFailed("Payment Failed")
            else:
               raise InvalidCerdiantials("Invalid Paymnent Options")
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise
        except (PaymentFailed, InvalidCerdiantials):
            delete_order = self.__order_service.cancel_my_order(order_id)
            raise

            
                    

                
                    



        