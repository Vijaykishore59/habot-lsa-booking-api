from app import create_app
from app.extensions import db
from app.models.lsa_profile import LSAProfile

app = create_app()

with app.app_context():
    lsa1 = LSAProfile(
        name="Ananya Sharma",
        email="ananya@example.com",
        skills="Autism, ADHD, Dyslexia",
        hourly_rate=25.00,
        is_active=True
    )

    lsa2 = LSAProfile(
        name="Rahul Mehta",
        email="rahul@example.com",
        skills="ADHD, Speech Therapy",
        hourly_rate=30.00,
        is_active=True
    )

    lsa3 = LSAProfile(
        name="Priya Rao",
        email="priya@example.com",
        skills="Dyslexia, Learning Support",
        hourly_rate=28.00,
        is_active=False
    )

    db.session.add_all([lsa1, lsa2, lsa3])
    db.session.commit()

    print("LSA test data inserted successfully.")