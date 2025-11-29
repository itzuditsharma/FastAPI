from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def send_email(email: str, message: str):
    time.sleep(3)
    print(f"Email sent successfully to {email} : {message}")

@app.post("/notify")
def notify(email: str, message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, message)
    return {"status" : "Email will be sent in background"}