# HabotConnect – LSA Booking API

A Flask-based REST API for managing Learning Support Assistants (LSAs), parents, booking requests, and payment processing.

The API provides LSA search, booking creation, booking conflict prevention, payment webhook processing, and payment idempotency.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Database Design](#database-design)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Clone the Repository](#clone-the-repository)
- [Create Virtual Environment](#create-virtual-environment)
- [Activate Virtual Environment](#activate-virtual-environment)
- [Install Dependencies](#install-dependencies)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Seed Test Data](#seed-test-data)
- [Run the Application](#run-the-application)
- [Health Check](#health-check)
- [Swagger API Documentation](#swagger-api-documentation)
- [API Endpoints](#api-endpoints)
- [LSA Search](#lsa-search)
- [Create Booking](#create-booking)
- [Booking Validation](#booking-validation)
- [Double-Booking Prevention](#double-booking-prevention)
- [Payment Webhook](#payment-webhook)
- [Payment Idempotency](#payment-idempotency)
- [Booking and Payment Flow](#booking-and-payment-flow)
- [Testing](#testing)
- [GitHub Actions CI](#github-actions-ci)
- [Database Migrations](#database-migrations)
- [Git Workflow](#git-workflow)
- [Troubleshooting](#troubleshooting)
- [API Response Examples](#api-response-examples)
- [Future Improvements](#future-improvements)
- [Repository](#repository)
- [Author](#author)

---

# Project Overview

HabotConnect LSA Booking API is a backend application designed to manage the booking workflow between parents and Learning Support Assistants.

The system allows a parent to:

1. Search for LSAs based on skills.
2. View available LSA information.
3. Create a booking request.
4. Prevent overlapping bookings.
5. Process payment notifications.
6. Confirm a booking after successful payment.
7. Cancel a booking when payment fails.
8. Safely process duplicate payment webhooks using idempotency.

The application exposes REST APIs and provides interactive Swagger documentation.

---

# Features

## LSA Management

- LSA profile management.
- LSA skill information.
- LSA hourly rates.
- Active/inactive LSA status.
- Search LSAs by skills.

## Parent Management

- Parent information.
- Parent email and phone details.
- Parent-booking relationship.

## Booking Management

- Create booking requests.
- Validate booking time ranges.
- Validate parent and LSA references.
- Prevent overlapping bookings.
- Maintain booking status.
- Associate bookings with payments.

## Payment Management

- Payment records.
- Transaction ID tracking.
- Payment status tracking.
- Payment webhook processing.
- Booking confirmation after successful payment.
- Booking cancellation after failed payment.
- Duplicate webhook protection.

## Development

- Flask REST API.
- SQLAlchemy ORM.
- Flask-Migrate.
- SQLite database.
- Swagger API documentation.
- Pytest automated tests.
- GitHub Actions CI.

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Flask | Backend web framework |
| Flask-SQLAlchemy | SQLAlchemy integration |
| SQLAlchemy | ORM |
| Flask-Migrate | Database migrations |
| SQLite | Database |
| Flasgger | Swagger/OpenAPI documentation |
| Pytest | Automated testing |
| pytest-flask | Flask testing |
| Git | Version control |
| GitHub | Source code hosting |
| GitHub Actions | Continuous integration |

---

# System Architecture

```text
                    Client
                      |
                      v
              Flask REST API
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
    LSA Routes    Booking Routes   Payment Routes
        |             |             |
        +-------------+-------------+
                      |
                      v
                  Services
                      |
                      v
                 SQLAlchemy
                      |
                      v
                    SQLite
