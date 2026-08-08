from datetime import datetime, timezone

from app.extensions import db
from app.models.booking import BookingRequest
from app.models.lsa_profile import LSAProfile
from app.models.parent import Parent


class BookingValidationError(Exception):
    """Raised when booking validation fails."""


class ParentNotFoundError(Exception):
    """Raised when the parent does not exist."""


class LSANotFoundError(Exception):
    """Raised when the LSA does not exist."""


class BookingConflictError(Exception):
    """Raised when an LSA is already booked."""


def parse_datetime(value, field_name):
    if not value:
        raise BookingValidationError(
            f"{field_name} is required."
        )

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except (ValueError, AttributeError):
        raise BookingValidationError(
            f"{field_name} must be a valid ISO 8601 datetime."
        )


def create_booking(data):
    if not isinstance(data, dict):
        raise BookingValidationError(
            "Request body must be a JSON object."
        )

    required_fields = [
        "parent_id",
        "lsa_id",
        "start_time",
        "end_time",
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        raise BookingValidationError(
            f"Missing required fields: {', '.join(missing_fields)}."
        )

    parent = db.session.get(
        Parent,
        data["parent_id"]
    )

    if not parent:
        raise ParentNotFoundError(
            "Parent not found."
        )

    lsa = db.session.get(
        LSAProfile,
        data["lsa_id"]
    )

    if not lsa:
        raise LSANotFoundError(
            "LSA not found."
        )

    if not lsa.is_active:
        raise BookingValidationError(
            "LSA is not active."
        )

    start_time = parse_datetime(
        data["start_time"],
        "start_time"
    )

    end_time = parse_datetime(
        data["end_time"],
        "end_time"
    )

    if start_time.tzinfo is None:
        start_time = start_time.replace(
            tzinfo=timezone.utc
        )

    if end_time.tzinfo is None:
        end_time = end_time.replace(
            tzinfo=timezone.utc
        )

    if start_time >= end_time:
        raise BookingValidationError(
            "start_time must be earlier than end_time."
        )

    overlapping_booking = BookingRequest.query.filter(
        BookingRequest.lsa_id == lsa.id,
        BookingRequest.status.in_(
            ["PENDING", "CONFIRMED"]
        ),
        BookingRequest.start_time < end_time,
        BookingRequest.end_time > start_time
    ).first()

    if overlapping_booking:
        raise BookingConflictError(
            "LSA is already booked for the requested time."
        )

    booking = BookingRequest(
        parent_id=parent.id,
        lsa_id=lsa.id,
        start_time=start_time,
        end_time=end_time,
        status="PENDING",
        notes=data.get("notes")
    )

    db.session.add(booking)
    db.session.commit()

    return booking