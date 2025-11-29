from fastapi import FastAPI, HTTPException
app = FastAPI()

articles = [
    {"id": i, "title" : f"Article {i}", "author" : "Author A"} for i in range(1,51)
]

@app.get("/articles")
def get_articles(page: int = 1, limit: int = 10):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail = "Page and limit must be positive")
    
    start = (page - 1) * limit
    end = start + limit

    return {
        "items" : articles[start:end],
        "total" : len(articles),
        "page" : page,
        "limit" : limit
    }