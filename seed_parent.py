from app import create_app
from app.extensions import db
from app.models.parent import Parent

app = create_app()

with app.app_context():
    parent = Parent(
        name="Vijay Kumar",
        email="parent@example.com",
        phone="9876543210"
    )

    db.session.add(parent)
    db.session.commit()

    print(f"Parent created successfully. ID: {parent.id}")