from celery_worker import celery
from app.extensions import db
from app.models import AudioFile, AudioAnalysis

import librosa
import numpy as np
import os


@celery.task(bind=True)
def analyze_audio(self, audio_id):
    audio = AudioFile.query.get(audio_id)

    if not audio:
        return "Audio not found"

    try:
        # 🔹 Статус: обработка
        audio.status = "processing"
        db.session.commit()

        file_path = audio.file_path

        if not os.path.exists(file_path):
            raise FileNotFoundError("Audio file not found on disk")

        # 🔹 Загрузка аудио
        y, sr = librosa.load(file_path, sr=None)

        # 🔹 БАЗОВЫЕ ХАРАКТЕРИСТИКИ
        duration = librosa.get_duration(y=y, sr=sr)

        rms = librosa.feature.rms(y=y)
        rms_mean = float(np.mean(rms))

        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = float(np.mean(spectral_centroid))

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1).tolist()

        # 🔹 Сохранение в БД
        analysis = AudioAnalysis(
            audio_id=audio.id,
            duration=duration,
            sample_rate=sr,
            rms_mean=rms_mean,
            spectral_centroid_mean=spectral_centroid_mean,
            mfcc=mfcc_mean,
        )

        db.session.add(analysis)

        # 🔹 Статус: готово
        audio.status = "done"
        db.session.commit()

        return "Analysis completed"

    except Exception as e:
        audio.status = "error"
        db.session.commit()
        return str(e)
