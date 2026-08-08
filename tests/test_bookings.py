from datetime import datetime, timezone

from app.extensions import db
from app.models.booking import BookingRequest
from app.models.lsa_profile import LSAProfile
from app.models.parent import Parent


def create_test_data():
    parent = Parent(
        name="Test Parent",
        email="testparent@example.com",
        phone="9876543210",
    )

    lsa = LSAProfile(
        name="Test LSA",
        email="testlsa@example.com",
        skills="Autism, ADHD",
        hourly_rate=25.00,
        is_active=True,
    )

    db.session.add_all([parent, lsa])
    db.session.commit()

    return parent, lsa


def test_booking_creation(client, app):
    with app.app_context():
        parent, lsa = create_test_data()

        response = client.post(
            "/api/v1/bookings/",
            json={
                "parent_id": parent.id,
                "lsa_id": lsa.id,
                "start_time": "2026-08-10T10:00:00+00:00",
                "end_time": "2026-08-10T11:00:00+00:00",
                "notes": "Test booking",
            },
        )

        assert response.status_code == 201

        data = response.get_json()

        assert data["status"] == "success"
        assert data["data"]["status"] == "PENDING"


def test_overlapping_booking_is_rejected(client, app):
    with app.app_context():
        parent, lsa = create_test_data()

        first_booking = BookingRequest(
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

        db.session.add(first_booking)
        db.session.commit()

        response = client.post(
            "/api/v1/bookings/",
            json={
                "parent_id": parent.id,
                "lsa_id": lsa.id,
                "start_time": "2026-08-10T10:30:00+00:00",
                "end_time": "2026-08-10T11:30:00+00:00",
            },
        )

        assert response.status_code == 409

        data = response.get_json()

        assert data["status"] == "error"
        assert (
            data["message"]
            == "LSA is already booked for the requested time."
        )
def test_invalid_booking_is_rejected(client, app):
    with app.app_context():
        parent, lsa = create_test_data()

        response = client.post(
            "/api/v1/bookings/",
            json={
                "parent_id": parent.id,
                "lsa_id": lsa.id,
                "start_time": "2026-08-10T10:00:00+00:00",
                "end_time": "2026-08-10T09:00:00+00:00",
                "notes": "Invalid time range",
            },
        )

        assert response.status_code in [400, 422]