from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.reservation import Reservation
from app.shcemas.reservation_schema import ReservationSchema
from app.extensions import db
from marshmallow import ValidationError

reservation_bp = Blueprint("reservations", __name__, url_prefix="/api/reservations")

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)