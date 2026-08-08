from datetime import datetime, timezone

from app.extensions import db


class LSAProfile(db.Model):
    __tablename__ = "lsa_profiles"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)

    skills = db.Column(db.String(500), nullable=False)

    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    bookings = db.relationship(
        "BookingRequest",
        back_populates="lsa",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<LSAProfile {self.name}>"