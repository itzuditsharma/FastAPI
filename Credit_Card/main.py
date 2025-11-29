from fastapi import FastAPI, HTTPException
from pydantic import Field, BaseModel
from typing import Literal, Annotated

app = FastAPI()

class Applicant(BaseModel):
    age: Annotated[int, Field(strict=True, gt=17)]
    education: Literal["high_school", "graduation", "masters", "phd"]
    marital_status: Literal["single", "married"]
    salary: Annotated[float, Field(strict=True, gt=0)]

class Response(BaseModel):
    eligible: bool
    score: float

@app.post("/predict")
def predict(applicant: Applicant):
    score = 0.0
    # dummy scoring 

    if applicant.age > 25:
        score += 10
    
    if applicant.salary > 50000:
        score += 50
    else:
        score += applicant.salary / 1000
    
    if applicant.education in ["phd", "masters"]:
        score += 20
    
    eligible = score >= 60

    return Response(eligible=eligible, score=score)
