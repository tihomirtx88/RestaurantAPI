from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.reservation import Reservation
from app.shcemas.reservation_schema import ReservationSchema
from app.extensions import db
from marshmallow import ValidationError

reservation_bp = Blueprint("reservations", __name__, url_prefix="/api/reservations")

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

@reservation_bp.route("/", methods=["POST"])
@jwt_required()
def create_reservation():

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data"}), 400

    try:
        reservation = reservation_schema.load(data)
        reservation.user_id = user_id

    except ValidationError as err:
        return jsonify(err.messages), 400


    db.session.add(reservation)
    db.session.commit()

    return reservation_schema.dump(reservation), 201