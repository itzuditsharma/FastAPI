from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional

app = FastAPI()

API_TOKEN = "mysecretstoken123"

def verify_token(x_token : Optional[str] = Header(None)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return True

@app.get("/secrets-data")
def get_secrets_data(auth: bool = Depends(verify_token)):
    return {"secrets_data" : "This is the text visible to authenticated user"}