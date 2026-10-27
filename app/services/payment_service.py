from app.repositories import PaymentsRepo, OrdersRepo
from datetime import datetime, date, time
from typing import Any
class PaymentsService:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.payments_db = PaymentsRepo()
        self.orders_db = OrdersRepo()

    def generate_transaction_id(self) -> str:
        now = datetime.now()

        letters = "TXN"
        date_time = now.strftime("%Y%m%d%H%M%S%f")
        txn_id = letters + date_time
        return txn_id

    def make_transaction(self, order_id : str, amount : int, txn_method : str) -> dict[str, Any]:
        try:
            order_id = str(order_id)
            amount = int(amount)
            txn_method = str(txn_method)
            new_transaction = self.payments_db.create_transaction(
                txn_id= self.generate_transaction_id(),
                customer_id= self.customer_id,
                order_id= order_id,
                amount= amount,
                txn_method= txn_method
            )
            if not new_transaction:
                return{"success" : False, "message" : "Unable To Create Transaction", "data" : None}
            else:
                return{"success" : True, "message" : "Transaction Created Successfuly", "data" : new_transaction.txn_id}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "data" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e}", "data" : None}
        
    def make_payment(self, order_id : str, total_amount : int, payment_method : str, cerdinatals : str) -> dict[str, Any]: # need to add upi and card logic and self amount getter
        try:
            pay_options = ["COD", "UPI", "CARD"]
            order_id = str(order_id)
            order = self.orders_db.get_order(order_id) #order id must needed to exists
            if not order:
                return{"success" : False, "message" : "Invalid Order Id", "data" : None}
            if order.payment != "Not Paid":
                return{"success" : False, "message" : "Already Paid", "data" : None}
            total_amount = int(total_amount)
            payment_method = str(payment_method).upper()
            cerdinatals = str(cerdinatals)
            if payment_method in pay_options:
                if payment_method == "COD":
                    update_order = self.orders_db.update_status(order_id, "payment", "Not Paid(COD)")
                    if not update_order:
                        return{"success" : False, "message" : "Payment Failed", "data" : None}
                    return{"success" : True, "message" : "Payment Successful", "data" : None}
                elif payment_method == "UPI":
                    supporitng_partners = ("@upi", "@ybl", "@api", "@apl")
                    if cerdinatals.endswith(supporitng_partners):
                        transaction = self.make_transaction(order_id, total_amount, payment_method)
                        if transaction.get("success"):
                            update_order = self.orders_db.update_status(order_id, "payment", "Paid")
                            if not update_order:
                                delete_txn = self.payments_db.delete_transaction(transaction.get("data"))
                                return{"success" : False, "message" : "Payment Failed", "data" : None}
                            return{"success" : True, "message" : "Payment Successful", "data" : transaction.get("data")}
                        else:
                            return{"success" : False, "message" : "Payment Failed", "data" : None}
                    else:
                        return{"success" : False, "message" : "Sorry We Can't Accept The UPI Id Now", "data" : None}

                elif payment_method == "Card":
                    if len(cerdinatals) != 16:
                        return{"success" : False, "message" : "Payment Failed, Invalid Card Number", "data" : None}
                    transaction = self.make_transaction(order_id, total_amount, payment_method)
                    if transaction.get("success"):
                        update_order = self.orders_db.update_status(order_id, "payment", "Paid")
                        if not update_order:
                            delete_txn = self.payments_db.delete_transaction(transaction.get("data"))
                            return{"success" : False, "message" : "Payment Failed", "data" : None}

                        return{"success" : True, "message" : "Payment Successful", "data" : transaction.get("data")}
                    else:
                        return{"success" : False, "message" : "Payment Failed", "data" : None}
            else:
                return{"success" : False, "message" : "Invalid Payment Options", "data" : None}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "data" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e}", "data" : None}
            
                    

                
                    



        