from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models
    from app.routes.auth import auth_bp
    from app.routes.audio import audio_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(audio_bp)

    return app
