from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from app.shcemas.review_schema import ReviewSchema
from app.extensions import db
from marshmallow import ValidationError

review_bp = Blueprint("reviews", __name__, url_prefix="/api/reviews")

# Schema instances
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@review_bp.route("/", methods=["POST"])
@jwt_required()
def create_review():

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data"}), 400

    try:
        review = review_schema.load(data)
        review.user_id = user_id

    except ValidationError as err:
        return jsonify(err.messages), 400


    db.session.add(review)
    db.session.commit()

    return review_schema.dump(review), 201

@review_bp.route("/menu/<int:menu_id>", methods=["GET"])
def get_reviews(menu_id):

    reviews = Review.query.filter_by(menu_item_id=menu_id).all()

    return reviews_schema.dump(reviews), 200