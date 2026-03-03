from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.review import Review
from marshmallow import fields

class ReviewSchema(SQLAlchemyAutoSchema):

    user = fields.String(attribute="user.email")
    menu_item = fields.String("menu_item.name")

    class Meta:
        model = Review
        load_instance = True
        include_fk = True