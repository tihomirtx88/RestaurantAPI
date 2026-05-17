from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.category import Category

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        include_relationships = True