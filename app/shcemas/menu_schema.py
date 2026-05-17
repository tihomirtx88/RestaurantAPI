from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.menu_item import MenuItem
from marshmallow import fields
from app.extensions import db

class MenuItemSchema(SQLAlchemyAutoSchema):
    category = fields.String(attribute="category.name", dump_only=True)

    class Meta:
        model = MenuItem
        load_instance = True
        include_fk = True
        sqla_session = db.session
