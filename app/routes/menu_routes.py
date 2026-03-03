from flask import Blueprint, request, jsonify
from app.models.menu_item import MenuItem
from app.models.category import Category
from app.shcemas.menu_schema import MenuItemSchema
from app.extensions import db

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