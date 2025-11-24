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