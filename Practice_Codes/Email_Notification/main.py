from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def send_email(email: str, message: str):
    time.sleep(3)
    print(f"Email sent to {email}: {message}")

@app.post("/notify")
def notify(email: str, message: str, background_task: BackgroundTasks):
    background_task.add_task(send_email, email, message)
    return {f"Hi, {email} your order is placed."}