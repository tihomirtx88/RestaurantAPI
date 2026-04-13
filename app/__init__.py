from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, bcrypt, mail
from app.routes.auth_routes import auth_bp

from .models.user import User
from .models.token_blocklist import TokenBlocklist
from .models.category import Category
from .models.menu_item import MenuItem
from .models.reservation import Reservation
from .models.review import Review

from app.routes.category_routes import category_bp
from .routes.review_routes import review_bp
from .routes.menu_routes import menu_bp
from .routes.reservation_routes import reservation_bp

from app.utilis.error_handler import register_error_handlers

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return TokenBlocklist.query.filter_by(jti=jti).first() is not None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Register Global Error Handler
    register_error_handlers(app)

    @app.route("/")
    def home():
        return {"message": "Restaurant API running 🚀"}

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(category_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(reservation_bp)

    return app