from fastapi import FastAPI
from celery.result import AsyncResult
from pydantic import BaseModel, EmailStr
from worker import send_background_email, generate_pdf_report

app = FastAPI(title="Day 20: FastAPI + Celery Interactive")

# Pydantic schema for validating the incoming email request
class EmailPayload(BaseModel):
    email: EmailStr
    subject: str


@app.post("/send-email/", status_code=202)
def trigger_email(payload: EmailPayload):
    """Triggers the background email task and returns an ID instantly."""
    
    # .delay() tells Celery to push this job to Redis and keep moving
    task = send_background_email.delay(payload.email, payload.subject)
    
    return {
        "message": "Email task dispatched successfully!",
        "task_id": task.id,
        "current_status": task.status
    }


@app.get("/task/{task_id}")
def check_task_status(task_id: str):
    """Checks the real-time state and result of a specific background task."""
    
    # Look up the task using its unique tracking ID from the Redis backend
    task_result = AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,  # Will be PENDING, STARTED, SUCCESS, or FAILURE
        "result": None
    }
    
    # If the task finished executing, grab the return value
    if task_result.ready():
        response["result"] = task_result.result
        
    return response