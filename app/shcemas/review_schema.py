from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.review import Review
from marshmallow import fields
from app.extensions import db

class ReviewSchema(SQLAlchemyAutoSchema):

    user = fields.String(attribute="user.email", dump_only=True)
    menu_item = fields.String(attribute="menu_item.name", dump_only=True)

    class Meta:
        model = Review
        load_instance = True
        include_fk = True
        sqla_session = db.session