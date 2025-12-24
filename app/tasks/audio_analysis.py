from app.extensions import db
from app.models import AudioFile
from celery_worker import celery
import time

@celery.task(bind=True)
def analyze_audio(self, audio_id):
    audio = AudioFile.query.get(audio_id)

    if not audio:
        return "Audio not found"

    try:
        # 1. Статус: обработка
        audio.status = "processing"
        db.session.commit()

        # 2. Имитация тяжёлой работы
        time.sleep(5)

        # 3. Статус: готово
        audio.status = "done"
        db.session.commit()

        return "Analysis completed"

    except Exception as e:
        audio.status = "error"
        db.session.commit()
        return str(e)
