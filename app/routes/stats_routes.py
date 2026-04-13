from flask import Blueprint
from app.models.reservation import Reservation
from app.models.review import Review
from app.models.menu_item import MenuItem
from app.extensions import db
from app.utilis.error_handler import AppError

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")