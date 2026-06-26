from celery import Celery

# 1. Define where the Redis broker and result backend live
REDIS_URL = "redis://localhost:6379/0"

# 2. Fire up the Celery instance and give it a name ('tasks')
celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# 3. Optional adjustments for smooth operation
celery_app.conf.update(
    task_track_started=True,
    result_expires=3600  # Automatically cleans up old results from Redis after 1 hour
)
import time
import logging

# Set up logging so we can see the worker action clearly in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task
def send_background_email(user_email: str, subject: str):
    """Simulates sending a real email by sleeping for 3 seconds."""
    logger.info(f"📧 Starting email delivery sequence to {user_email}...")
    
    time.sleep(3)  # Simulating network lag with an email provider
    
    logger.info(f"✨ Email successfully delivered to {user_email}!")
    return {"status": "Sent", "to": user_email}


@celery_app.task
def generate_pdf_report(report_id: int):
    """Simulates a heavy CPU-bound PDF/CSV generation task."""
    logger.info(f"📊 Crunching numbers for heavy PDF report #{report_id}...")
    
    time.sleep(5)  # Simulating complex data compilation
    
    logger.info(f"✅ PDF report #{report_id} has been built and cached.")
    return {"status": "Ready", "download_url": f"/downloads/report_{report_id}.pdf"}