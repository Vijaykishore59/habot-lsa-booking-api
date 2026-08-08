# Habot LSA Booking API

A Flask-based backend for managing Learning Support Assistant (LSA) profiles, parent booking requests, and payment processing.

The project provides REST APIs for searching LSAs, creating bookings, preventing overlapping bookings, and processing payment webhooks with idempotency protection.

## Features

- LSA profile management
- LSA search by skills
- Parent and booking management
- Booking time validation
- Prevention of overlapping LSA bookings
- Payment record management
- Payment webhook processing
- Idempotent payment webhook handling
- SQLAlchemy ORM
- Flask-Migrate database migrations
- Swagger API documentation
- Automated pytest test suite
- GitHub Actions CI

## Tech Stack

- Python 3.12
- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite
- Flasgger / Swagger
- Pytest
- GitHub Actions

## Project Structure

```text
habot-lsa-booking/
│
├── app/
│   ├── models/
│   │   ├── booking.py
│   │   ├── lsa_profile.py
│   │   ├── parent.py
│   │   └── payment.py
│   │
│   ├── routes/
│   │   ├── bookings.py
│   │   ├── lsas.py
│   │   └── payments.py
│   │
│   ├── services/
│   │   └── payment_service.py
│   │
│   ├── extensions.py
│   └── __init__.py
│
├── migrations/
├── tests/
│   ├── conftest.py
│   ├── test_bookings.py
│   └── test_payments.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── run.py
├── seed.py
├── seed_payment.py
├── requirements.txt
└── README.md
