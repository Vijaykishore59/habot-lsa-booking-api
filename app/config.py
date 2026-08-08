import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///habot.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PAYMENT_SERVICE_URL = os.getenv(
        "PAYMENT_SERVICE_URL",
        "https://example.com/payment"
    )