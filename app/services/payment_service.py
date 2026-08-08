from app.extensions import db
from app.models.payment import Payment
from app.models.booking import BookingRequest


class PaymentValidationError(Exception):
    """Raised when payment validation fails."""


class PaymentNotFoundError(Exception):
    """Raised when a payment does not exist."""


class DuplicateWebhookError(Exception):
    """Raised when a webhook event was already processed."""


def create_payment(booking_id, amount):
    booking = db.session.get(
        BookingRequest,
        booking_id
    )

    if not booking:
        raise PaymentValidationError(
            "Booking not found."
        )

    # One payment per booking
    existing_payment = Payment.query.filter_by(
        booking_id=booking.id
    ).first()

    if existing_payment:
        return existing_payment

    payment = Payment(
        booking_id=booking.id,
        amount=amount,
        status="PENDING"
    )

    db.session.add(payment)
    db.session.commit()

    return payment


def process_payment_webhook(data):
    if not isinstance(data, dict):
        raise PaymentValidationError(
            "Request body must be a JSON object."
        )

    required_fields = [
        "transaction_id",
        "booking_id",
        "status",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        raise PaymentValidationError(
            f"Missing required fields: "
            f"{', '.join(missing_fields)}."
        )

    transaction_id = data["transaction_id"]
    booking_id = data["booking_id"]
    status = data["status"].upper()

    if status not in ["SUCCESS", "FAILED"]:
        raise PaymentValidationError(
            "status must be SUCCESS or FAILED."
        )

    # Idempotency:
    # If this transaction was already processed,
    # don't process it again.
    existing_transaction = Payment.query.filter_by(
        transaction_id=transaction_id
    ).first()

    if existing_transaction:
        return existing_transaction, False

    payment = Payment.query.filter_by(
        booking_id=booking_id
    ).first()

    if not payment:
        raise PaymentNotFoundError(
            "Payment not found for booking."
        )

    payment.transaction_id = transaction_id
    payment.status = status

    if status == "SUCCESS":
        payment.booking.status = "CONFIRMED"

    elif status == "FAILED":
        payment.booking.status = "CANCELLED"

    db.session.commit()

    return payment, True