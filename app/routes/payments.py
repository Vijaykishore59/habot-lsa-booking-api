from flask import Blueprint, jsonify, request

from app.extensions import db
from app.services.payment_service import (
    DuplicateWebhookError,
    PaymentNotFoundError,
    PaymentValidationError,
    process_payment_webhook,
)


payments_bp = Blueprint(
    "payments",
    __name__,
    url_prefix="/api/v1/payments"
)


@payments_bp.post("/webhook/")
def payment_webhook():
    """
    Process payment webhook
    ---
    tags:
      - Payments

    consumes:
      - application/json

    parameters:
      - in: body
        name: payment
        required: true
        schema:
          type: object
          required:
            - transaction_id
            - booking_id
            - status
          properties:
            transaction_id:
              type: string
              example: TXN_10001
            booking_id:
              type: integer
              example: 1
            status:
              type: string
              enum:
                - SUCCESS
                - FAILED
              example: SUCCESS

    responses:
      200:
        description: Webhook processed successfully

      400:
        description: Invalid webhook payload

      404:
        description: Payment not found

      500:
        description: Internal server error
    """

    try:
        data = request.get_json(silent=True)

        payment, processed = process_payment_webhook(
            data
        )

        return jsonify({
            "status": "success",
            "message": (
                "Webhook processed successfully."
                if processed
                else "Webhook already processed."
            ),
            "data": {
                "payment_id": payment.id,
                "booking_id": payment.booking_id,
                "transaction_id": payment.transaction_id,
                "status": payment.status,
                "booking_status": payment.booking.status,
            }
        }), 200

    except PaymentValidationError as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 400

    except PaymentNotFoundError as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 404

    except Exception:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred."
        }), 500