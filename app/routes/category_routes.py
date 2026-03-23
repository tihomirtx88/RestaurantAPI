from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.shcemas.category_schema import CategorySchema
from app.extensions import db

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@category_bp.route("/", methods=["GET"])
def get_categories():
    sort = request.args.get("sort", "order")

    categories = Category.query.order_by(sort).all()
    return categories_schema.dump(categories), 200