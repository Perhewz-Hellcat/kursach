import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import AudioFile

audio_bp = Blueprint("audio", __name__, url_prefix="/api/audio")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@audio_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_audio():
    if "file" not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Unsupported file format"}), 400

    user_id = int(get_jwt_identity())

    filename = secure_filename(file.filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    audio = AudioFile(user_id=user_id, original_filename=filename, file_path=file_path)

    db.session.add(audio)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "audio_id": audio.id}), 201
