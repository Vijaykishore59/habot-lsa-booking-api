from datetime import datetime, timezone

from app.extensions import db
from app.models.booking import BookingRequest
from app.models.lsa_profile import LSAProfile
from app.models.parent import Parent
from app.models.payment import Payment


def create_booking():
    parent = Parent(
        name="Test Parent",
        email="paymentparent@example.com",
        phone="9876543210",
    )

    lsa = LSAProfile(
        name="Test LSA",
        email="paymentlsa@example.com",
        skills="Autism",
        hourly_rate=25.00,
        is_active=True,
    )

    db.session.add_all([parent, lsa])
    db.session.commit()

    booking = BookingRequest(
    parent_id=parent.id,
    lsa_id=lsa.id,
    start_time=datetime(
        2026, 8, 10, 10, 0,
        tzinfo=timezone.utc
    ),
    end_time=datetime(
        2026, 8, 10, 11, 0,
        tzinfo=timezone.utc
    ),
    status="PENDING",
)

    db.session.add(booking)
    db.session.commit()

    payment = Payment(
        booking_id=booking.id,
        amount=25.00,
        status="PENDING",
    )

    db.session.add(payment)
    db.session.commit()

    return booking


def test_payment_webhook_success(client, app):
    with app.app_context():
        booking = create_booking()

        response = client.post(
            "/api/v1/payments/webhook/",
            json={
                "transaction_id": "TXN_TEST_001",
                "booking_id": booking.id,
                "status": "SUCCESS",
            },
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "success"
        assert data["data"]["status"] == "SUCCESS"
        assert data["data"]["booking_status"] == "CONFIRMED"


def test_payment_webhook_is_idempotent(client, app):
    with app.app_context():
        booking = create_booking()

        payload = {
            "transaction_id": "TXN_TEST_002",
            "booking_id": booking.id,
            "status": "SUCCESS",
        }

        first_response = client.post(
            "/api/v1/payments/webhook/",
            json=payload,
        )

        second_response = client.post(
            "/api/v1/payments/webhook/",
            json=payload,
        )

        assert first_response.status_code == 200
        assert second_response.status_code == 200

        first_data = first_response.get_json()
        second_data = second_response.get_json()

        assert (
            first_data["message"]
            == "Webhook processed successfully."
        )

        assert (
            second_data["message"]
            == "Webhook already processed."
        )

        assert Payment.query.count() == 1