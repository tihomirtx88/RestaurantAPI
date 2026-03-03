from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.menu_item import MenuItem
from marshmallow import fields

class MenuItemSchema(SQLAlchemyAutoSchema):
    category = fields.String(attribute="category.name")

    class Meta:
        model = MenuItem
        load_instance = True
        include_fk = True