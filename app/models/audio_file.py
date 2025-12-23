from datetime import datetime
from app.extensions import db


class AudioFile(db.Model):
    __tablename__ = "audio_files"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="uploaded")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audio_files")

    def __repr__(self):
        return f"<AudioFile {self.original_filename}>"
