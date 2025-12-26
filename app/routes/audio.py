import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import AudioFile
from app.models import AudioAnalysis

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

    from app.tasks.audio_analysis import analyze_audio

    analyze_audio.delay(audio.id)

    return jsonify({"message": "File uploaded successfully", "audio_id": audio.id}), 201


@audio_bp.route("/<int:audio_id>", methods=["GET"])
@jwt_required()
def get_audio_info(audio_id):
    user_id = get_jwt_identity()

    audio = AudioFile.query.filter_by(id=audio_id, user_id=user_id).first()

    if not audio:
        return {"message": "Audio not found"}, 404

    return {
        "id": audio.id,
        "original_filename": audio.original_filename,
        "status": audio.status,
        "created_at": audio.created_at.isoformat(),
    }, 200


@audio_bp.route("/<int:audio_id>/analysis", methods=["GET"])
@jwt_required()
def get_audio_analysis(audio_id):
    user_id = get_jwt_identity()

    audio = AudioFile.query.filter_by(id=audio_id, user_id=user_id).first()

    if not audio:
        return {"message": "Audio not found"}, 404

    if audio.status != "done":
        return {"message": "Analysis not completed", "status": audio.status}, 400

    analysis = AudioAnalysis.query.filter_by(audio_id=audio.id).first()

    if not analysis:
        return {"message": "Analysis data not found"}, 404

    return {
        "audio_id": audio.id,
        "duration": analysis.duration,
        "sample_rate": analysis.sample_rate,
        "rms_mean": analysis.rms_mean,
        "spectral_centroid_mean": analysis.spectral_centroid_mean,
        "mfcc": analysis.mfcc,
    }, 200


@audio_bp.route("/<int:audio_id>/visualization", methods=["GET"])
@jwt_required()
def get_audio_visualization(audio_id):
    user_id = get_jwt_identity()

    audio = AudioFile.query.filter_by(id=audio_id, user_id=user_id).first()

    if not audio or not audio.analysis:
        return {"message": "Visualization data not found"}, 404

    return {
        "waveform": audio.analysis.waveform,
        "fft": audio.analysis.fft,
        "mfcc": audio.analysis.mfcc,
    }, 200


@audio_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_audios():
    user_id = get_jwt_identity()

    audios = AudioFile.query.filter_by(user_id=user_id).all()

    return [
        {
            "id": a.id,
            "filename": a.original_filename,
            "status": a.status,
            "created_at": a.created_at.isoformat(),
        }
        for a in audios
    ], 200
