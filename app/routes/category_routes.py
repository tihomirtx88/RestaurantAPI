from flask import Blueprint, request
from app.models.category import Category
from app.shcemas.category_schema import CategorySchema
from app.extensions import db
from marshmallow import ValidationError
from app.utilis.permissions import role_required

from app.utilis.app_error import AppError

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
        return AppError("No input data", 400)

    try:
        category = category_schema.load(data)
    except ValidationError as err:
        raise AppError(err.messages, 400)
    except Exception as e:
        raise e

    db.session.add(category)
    db.session.commit()

    return category_schema.dump(category), 201