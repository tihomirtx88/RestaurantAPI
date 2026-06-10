import os
import uuid

from werkzeug.utils import secure_filename
from flask import Blueprint, request, current_app

upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/upload"
)