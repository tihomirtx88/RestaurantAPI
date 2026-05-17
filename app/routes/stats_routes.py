from flask import Blueprint
from app.models.reservation import Reservation
from app.models.review import Review
from app.models.menu_item import MenuItem
from app.extensions import db
from app.utilis.cache import get_cache, set_cache

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")

@stats_bp.route("/", methods=["GET"])
def get_stats():

    cached = get_cache("stats")

    if cached:
        return cached, 200

    # Total reservation
    total_reservations = Reservation.query.count()
    # Avg rating
    avg_rating = db.session.query(
        db.func.avg(Review.rating)
    ).scalar()

    # Most popular dishes
    popular_items = db.session.query(
        MenuItem.name,
        db.func.count(Review.id).label("reviews_count")
    ).join(Review).group_by(MenuItem.id).order_by(
        db.func.count(Review.id).desc()
    ).limit(5).all()

    # Reservation by day
    reservations_per_day = db.session.query(
        db.func.date(Reservation.reservation_date),
        db.func.count(Reservation.id)
    ).group_by(
        db.func.date(Reservation.reservation_date)
    ).all()


    response = {
        "total_reservations": total_reservations,
        "average_rating": float(avg_rating) if avg_rating else 0,
        "popular_items": [
            {"name": item[0], "reviews": item[1]}
            for item in popular_items
        ],
        "reservations_per_day": [
            {"date": str(day[0]), "count": day[1]}
            for day in reservations_per_day
        ]
    }

    set_cache("stats", response, ttl=60)

    return response, 200


