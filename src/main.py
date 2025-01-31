from fastapi import FastAPI
from routers import author, article, category

app = FastAPI()
app.include_router(author.router)
app.include_router(article.router)
app.include_router(category.router)
