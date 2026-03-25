from flask import Blueprint, request, jsonify
from app.models.menu_item import MenuItem
from app.models.category import Category
from app.shcemas.menu_schema import MenuItemSchema
from app.extensions import db
from flask_jwt_extended import jwt_required

menu_bp = Blueprint("menu", __name__, url_prefix="/api/menu")

# Schema instances
menu_schema = MenuItemSchema()
menus_schema = MenuItemSchema(many=True)

# -------------------------
# GET ALL MENU ITEMS
# -------------------------
@menu_bp.route("/", methods=["GET"])
def get_menu():

    category_name = request.args.get("category")

    query = MenuItem.query

    if category_name:
        category = Category.query.filter_by(name=category_name.capitalize()).first()

        if not query:
            return jsonify({"message": "Category not found"}), 404

        query = query.filter_by(category_id=category.id)

    items = query.all()

    return menus_schema.dump(items), 200

# -------------------------
# GET ALL MENU ITEMS WITH FILTERING
# -------------------------

@menu_bp.route("/filter", methods=["GET"])
def get_filter_menu():

    category_name = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    sort = request.args.get("sort", "id")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    query = MenuItem.query

    if category_name:
        category = Category.query.filter_by(
            name=category_name.capitalize()
        ).first()
        if category:
            query = query.filter_by(category_id=category.id)

    if min_price:
        query = query.filter(MenuItem.price >= float(min_price))

    if max_price:
        query = query.filter(MenuItem.price <= float(max_price))

    if sort == "price":
        query = query.order_by(MenuItem.price)
    elif sort == "name":
        query = query.order_by(MenuItem.name)
    else:
        query = query.order_by(MenuItem.id)

    paginated = query.paginate(page=page, per_page= per_page, error_out=False)

    return {
        "items": menus_schema.dump(paginated.items),
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages
    }, 200
