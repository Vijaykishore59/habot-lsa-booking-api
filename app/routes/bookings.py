from flask import Blueprint, jsonify, request

from app.extensions import db
from app.services.booking_service import (
    BookingConflictError,
    BookingValidationError,
    LSANotFoundError,
    ParentNotFoundError,
    create_booking,
)

bookings_bp = Blueprint(
    "bookings",
    __name__,
    url_prefix="/api/v1/bookings"
)


@bookings_bp.post("/")
def create_booking_endpoint():
    """
    Create a booking request
    ---
    tags:
      - Bookings

    consumes:
      - application/json

    parameters:
      - in: body
        name: booking
        required: true
        schema:
          type: object
          required:
            - parent_id
            - lsa_id
            - start_time
            - end_time
          properties:
            parent_id:
              type: integer
              example: 1
            lsa_id:
              type: integer
              example: 1
            start_time:
              type: string
              format: date-time
              example: "2026-08-10T10:00:00+00:00"
            end_time:
              type: string
              format: date-time
              example: "2026-08-10T11:00:00+00:00"
            notes:
              type: string
              example: "Initial learning support session"

    responses:
      201:
        description: Booking created successfully

      400:
        description: Invalid booking request

      404:
        description: Parent or LSA not found

      409:
        description: LSA already booked for the requested time

      500:
        description: Internal server error
    """

    try:
        data = request.get_json(silent=True)

        booking = create_booking(data)

        return jsonify({
            "status": "success",
            "message": "Booking created successfully.",
            "data": {
                "id": booking.id,
                "parent_id": booking.parent_id,
                "lsa_id": booking.lsa_id,
                "start_time": booking.start_time.isoformat(),
                "end_time": booking.end_time.isoformat(),
                "status": booking.status,
                "notes": booking.notes,
            }
        }), 201

    except BookingValidationError as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 400

    except ParentNotFoundError as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 404

    except LSANotFoundError as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 404

    except BookingConflictError as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 409

    except Exception:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred."
        }), 500