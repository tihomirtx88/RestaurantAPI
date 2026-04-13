from flask import jsonify
from app.utilis.app_error import AppError

def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            register_error_handlers
        }), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        print("ERROR:", error)

        return jsonify({
            "status": "error",
            "message": "Something went wrong"
        }), 500
