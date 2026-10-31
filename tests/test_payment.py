from app.services import PaymentsService


def test_payments():
    payment = PaymentsService(10212)

    pay = payment.make_payment("OD751313", 420000, "COD", "Cash On Delivery")
    assert pay.get("success") is True