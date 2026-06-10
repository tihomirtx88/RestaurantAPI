import os
import uuid

from werkzeug.utils import secure_filename
from flask import Blueprint, request, current_app

upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/upload"
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

def allowed_file(filename):

    return (
            "." in filename and
            filename.rsplit(".", 1)[1].lower()
            in ALLOWED_EXTENSIONS
    )

@upload_bp.route("/", methods=["POST"])
def upload_image():

    if "file" not in request.files:
        return {
            "message": "No file"
        }, 400

    file = request.files["file"]

    if file.filename == "":
        return {
            "message": "No selected file"
        }, 400

    if not allowed_file(file.filename):
        return {
            "message": "Invalid file type"
        }, 400

    ext = file.filename.rsplit(".", 1)[1]

    filename = (
        f"{uuid.uuid4()}.{ext}"
    )

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(upload_path)

    return {
        "image_url":
            f"/uploads/{filename}"
    }, 201