# HabotConnect – LSA Booking API

A Flask REST API for managing Learning Support Assistants (LSAs), parent booking requests, and payment processing.

## Features

- LSA search by skills
- Parent and LSA management
- Booking creation
- Booking time validation
- Double-booking prevention
- Payment webhook processing
- Payment webhook idempotency
- SQLite database with SQLAlchemy
- Flask-Migrate migrations
- Swagger API documentation
- Automated pytest tests
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

## Architecture

```text
Client
  │
  ▼
Flask REST API
  │
  ├── LSA Search
  ├── Booking Service
  └── Payment Webhook
          │
          ▼
      SQLAlchemy
          │
          ▼
        SQLite
