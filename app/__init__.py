from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()  # Create tables
        add_initial_entries()  # Add initial entries

    from .routes.main_routes import register_all

    register_all(app)

    return app


def add_initial_entries():
    from .models.user import User

    # Check if the database is empty before adding initial data
    if not User.query.first():
        initial_transactions = [
            User(name="Pranjal"),
            User(name="Medha")
        ]

        db.session.bulk_save_objects(initial_transactions)
        db.session.commit()

