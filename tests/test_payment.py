from app.services import PaymentsService


def test_payments():
    payment = PaymentsService(10212)

    pay = payment.make_payment("OD561628", 140000, "UPI", "9709988944@ybl")
    assert pay.order_id == "OD561628"