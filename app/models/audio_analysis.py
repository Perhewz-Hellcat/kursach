from app.extensions import db

class AudioAnalysis(db.Model):
    __tablename__ = "audio_analysis"

    id = db.Column(db.Integer, primary_key=True)
    audio_id = db.Column(db.Integer, db.ForeignKey("audio_files.id"), nullable=False)

    duration = db.Column(db.Float)
    sample_rate = db.Column(db.Integer)

    rms_mean = db.Column(db.Float)
    spectral_centroid_mean = db.Column(db.Float)

    mfcc = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
