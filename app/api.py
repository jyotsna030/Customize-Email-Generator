from fastapi import FastAPI, UploadFile, Form, HTTPException, WebSocket
from app.email_utils import send_email_smtp, personalize_email
from app.database import create_email_status, get_email_status
from tasks.celery_tasks import send_email_task
import pandas as pd
import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio

# Setup FastAPI and logging
app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Setup Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# WebSocket clients list
clients = []

# Function to handle sending emails
def send_email_logic(row, email_subject, email_body, smtp_server, smtp_port, email_account, email_password):
    personalized_body = personalize_email(email_body, row["name"], row.to_dict())
    send_email_smtp(row["email"], email_subject, personalized_body, smtp_server, smtp_port, email_account, email_password)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        data = pd.read_csv(file_location)
        os.remove(file_location)
        
        # Check if required columns are present
        if "email" not in data.columns or "name" not in data.columns:
            raise ValueError("Required columns 'email' and 'name' are missing.")
        
        return {"columns": list(data.columns)}

    except Exception as e:
        os.remove(file_location) if os.path.exists(file_location) else None
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send/")
@limiter.limit("5/minute")  # Limit to 5 requests per minute
async def send_emails_api(
    csv_file: UploadFile,
    smtp_server: str = Form(...),
    smtp_port: int = Form(...),
    email_account: str = Form(...),
    email_password: str = Form(...),
    email_subject: str = Form(...),
    email_body: str = Form(...),
):
    try:
        df = pd.read_csv(csv_file.file)
        statuses = []
        
        # Loop through each row and send email
        for _, row in df.iterrows():
            try:
                send_email_logic(row, email_subject, email_body, smtp_server, smtp_port, email_account, email_password)
                statuses.append({"email": row["email"], "status": "Sent"})
            except Exception as e:
                statuses.append({"email": row["email"], "status": str(e)})
        
        # Save email statuses to the database
        create_email_status(statuses)
        return {"status": "Emails sent", "details": statuses}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email sending: {str(e)}")

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # Fetch email statuses and send to WebSocket clients
            email_statuses = get_email_status()
            if email_statuses:
                await websocket.send_json(email_statuses)
            await asyncio.sleep(5)  # Poll every 5 seconds
    except Exception as e:
        clients.remove(websocket)
        logger.error(f"WebSocket error: {str(e)}")

@app.post("/schedule/")
async def schedule_emails_api(
    csv_file: UploadFile,
    smtp_server: str = Form(...),
    smtp_port: int = Form(...),
    email_account: str = Form(...),
    email_password: str = Form(...),
    email_subject: str = Form(...),
    email_body: str = Form(...),
):
    try:
        df = pd.read_csv(csv_file.file)
        
        # Schedule emails using Celery task
        for _, row in df.iterrows():
            send_email_task.delay(
                row["email"], email_subject, email_body, smtp_server, smtp_port, email_account, email_password
            )
        
        return {"status": "Emails scheduled"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling emails: {str(e)}")

@app.get("/status/")
async def get_status():
    try:
        return get_email_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching email statuses: {str(e)}")
