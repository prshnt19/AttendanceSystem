from attendance_system.celery import app

@app.task
def registering_voice():
    pass