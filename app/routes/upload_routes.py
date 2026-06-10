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