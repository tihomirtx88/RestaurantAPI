from flask import Blueprint, request
from app.utilis.error_handler import AppError

from app.extensions import db
from app.models.token_blocklist import TokenBlocklist
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        raise AppError("Email and password required", 400)

    if User.query.filter_by(email=data["email"]).first():
        raise AppError("Email already exists", 400)

    user = User(email=data["email"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
      raise AppError("Email and password required", 400)

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        raise AppError("Invalid credentials", 401)

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "user_id": user.id,
        "refresh_token": refresh_token
    }, 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    return {
        "email": user.email,
        "id": user.id
    }, 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)

    return {
        "access_token": new_access_token
    }, 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]

    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    return {"message": "Logged out"}, 200