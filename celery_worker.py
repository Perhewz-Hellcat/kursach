from app import create_app

app = create_app()
celery = app.celery

import app.tasks.audio_analysis
