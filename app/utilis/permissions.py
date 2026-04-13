from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Taking data from token
            jwt_data = get_jwt()

            # Taking role of user
            user_role = jwt_data.get("role")

            # cheks
            if user_role != required_role:
                return jsonify({"message": "Forbidden"}), 403

             # If everything is ok keep on to route
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Use @route("/admin")
# @jwt_required()
# @role_required("admin")
# def admin_panel():
#     return {"message": "Welcome admin"}
