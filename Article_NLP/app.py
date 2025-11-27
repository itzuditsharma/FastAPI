import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
import json
from typing import Literal, Optional, List

app = FastAPI()

class Article(BaseModel):
    title: str
    content: Optional[str] = None
    url: Optional[str] = None

class JobRequest(BaseModel):
    article_id: str
    tasks: List[str]

ARTICLES = "articles.json"
JOBS = "jobs.json"
RESULTS = "results.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)
    
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent = 4)

@app.post("/articles")
def upload_article(article: Article):
    articles = load_json(ARTICLES)
    article_id = str(uuid4())
    articles[article_id] = {
        "id" : article_id,
        "title" : article.title,
        "content" : article.content,
        "url" : article.url,
        "status" : "UPLOADED"
    }

    save_json(ARTICLES, articles)
    return {"article_id" : article_id, "status" : "UPLOADED"}

# 2036f322-9bc7-4f4d-90d9-7196badef9cf
@app.get("/articles/{article_id}")
def get_article(article_id: str):
    articles = load_json(ARTICLES)
    if article_id not in articles:
        raise HTTPException(404, "Article not found")

    return articles[article_id]

@app.post("/jobs")
def create_job(req: JobRequest):
    articles = load_json(ARTICLES)

    if req.article_id not in articles:
        raise HTTPException(404, "Invalid Article ID")
    
    jobs = load_json(JOBS)
    results = load_json(RESULTS)

    job_id = str(uuid4())
    result_id = str(uuid4())

    jobs[job_id] = {
        'id' : job_id,
        'article_id': req.article_id,
        'tasks': req.tasks,
        'status':"COMPLETED",
        'result_id': result_id
    }

    results[result_id] = {
        "result_id" : result_id,
        "summary" : "This is a placeholder summary",
        "sentiment" : "NEUTRAL",
        "entities": []
    }

    save_json(JOBS, jobs)
    save_json(RESULTS, results)

    return {"job_id": job_id, "status": "PROCESSING"}
