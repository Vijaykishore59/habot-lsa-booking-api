from datetime import datetime, timezone

from app.extensions import db


class BookingRequest(db.Model):
    __tablename__ = "booking_requests"

    id = db.Column(db.Integer, primary_key=True)

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("parents.id"),
        nullable=False,
        index=True
    )

    lsa_id = db.Column(
        db.Integer,
        db.ForeignKey("lsa_profiles.id"),
        nullable=False,
        index=True
    )

    start_time = db.Column(
        db.DateTime,
        nullable=False,
        index=True
    )

    end_time = db.Column(
        db.DateTime,
        nullable=False,
        index=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="PENDING",
        index=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    parent = db.relationship(
        "Parent",
        back_populates="bookings"
    )

    lsa = db.relationship(
        "LSAProfile",
        back_populates="bookings"
    )

    payment = db.relationship(
        "Payment",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index(
            "idx_booking_lsa_time",
            "lsa_id",
            "start_time",
            "end_time"
        ),
    )

    def __repr__(self):
        return f"<BookingRequest {self.id}>"