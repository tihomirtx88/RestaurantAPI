from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.reservation import Reservation
from app.shcemas.reservation_schema import ReservationSchema
from app.extensions import db
from marshmallow import ValidationError

from app.utilis.error_handler import AppError

reservation_bp = Blueprint("reservations", __name__, url_prefix="/api/reservations")

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

@reservation_bp.route("/", methods=["POST"])
@jwt_required()
def create_reservation():

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        raise AppError("No input data", 400)

    try:
        reservation = reservation_schema.load(data)
        reservation.user_id = user_id

    except ValidationError as err:
        raise AppError(err.messages, 400)


    db.session.add(reservation)
    db.session.commit()

    return reservation_schema.dump(reservation), 201

@reservation_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_reservations():

    user_id = get_jwt_identity()

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    return reservations_schema.dump(reservations), 200