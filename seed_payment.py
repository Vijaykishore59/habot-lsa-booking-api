from app import create_app
from app.extensions import db
from app.services.payment_service import create_payment


app = create_app()

with app.app_context():
    payment = create_payment(
        booking_id=1,
        amount=25.00
    )

    print(
        f"Payment created successfully. "
        f"ID: {payment.id}"
    )