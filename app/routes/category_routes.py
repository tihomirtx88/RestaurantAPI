from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.shcemas.category_schema import CategorySchema
from app.extensions import db
from marshmallow import ValidationError
from app.utilis.permissions import role_required

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

category_schema = CategorySchema(session=db.session)
categories_schema = CategorySchema(many=True, session=db.session)


@category_bp.route("/", methods=["GET"])
def get_categories():
    sort = request.args.get("sort", "order")

    if sort == "name":
        categories = Category.query.order_by(Category.name).all()
    else:
        categories = Category.query.order_by(Category.order).all()

    return categories_schema.dump(categories), 200


@category_bp.route("/", methods=["POST"])
@role_required("admin")
def create_category():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data"}), 400

    try:
        category = category_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

    db.session.add(category)
    db.session.commit()

    return category_schema.dump(category), 201