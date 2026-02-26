from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, bcrypt, mail
from .models.user import User
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    @app.route("/")
    def home():
        return {"message": "Restaurant API running 🚀"}

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app