from flask import jsonify
from app.utilis.app_error import AppError

def register_error_handlers(app):

    #Custom error
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            "status": "fail",
            "message": error.message
        }), error.status_code
    # All other errors
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        print("ERROR:", error)

        return jsonify({
            "status": "error",
            "message": "Something went wrong"
        }), 500
