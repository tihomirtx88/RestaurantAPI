from app.extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True, nullable=False)

    order = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship към MenuItem
    menu_items = db.relationship(
        "MenuItem",
        backref="category",
        lazy=True,
        cascade="all, delete-orphan"
    )

