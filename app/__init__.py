from flask import Flask
from flasgger import Swagger

from app.config import Config
from app.extensions import db, migrate
from app import models


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "openapi",
                "route": "/openapi.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
    }

    Swagger(
        app,
        config=swagger_config,
        template={
            "info": {
                "title": "Habot LSA Booking API",
                "description": "Backend API for the LSA Service Booking Platform",
                "version": "1.0.0",
            }
        },
    )

    from app.routes.bookings import bookings_bp
    from app.routes.lsas import lsas_bp
    from app.routes.payments import payments_bp

    app.register_blueprint(bookings_bp)
    app.register_blueprint(lsas_bp)
    app.register_blueprint(payments_bp)

    @app.get("/health")
    def health_check():
        return {
            "status": "success",
            "message": "Habot LSA Booking API is running"
        }, 200

    return app