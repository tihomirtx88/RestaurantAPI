from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.reservation import Reservation
from marshmallow import fields
from app.extensions import db

class ReservationSchema(SQLAlchemyAutoSchema):

    user = fields.String(attribute="user.email", dump_only=True)
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = Reservation
        load_instance = True
        include_fk = True
        sqla_session = db.session