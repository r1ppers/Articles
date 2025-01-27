import code
from datetime import date, datetime
from re import template
from turtle import title
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Body, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib

#Проверка на наличие объекта
def error_404(error_text: str, object_to_check: bool):
    if not object_to_check:
        raise HTTPException(status_code=404, detail=error_text)

#Хеширование пароля
def hash_password(password: str, author_login: str):
    password += password[0] + password[-1] + 'some_salt_for_hashing' + author_login
    password = hashlib.sha256(password.encode()).hexdigest()
    return password

app = FastAPI()
#Подключение шаблонов (HTML)
template = Jinja2Templates(directory="templates/HTML")
#Подключение статических файлов (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

class AuthorBase(BaseModel):
    first_name: str
    last_name: str 
    middle_name: str
    birth_date: date
    author_login: str
    author_password: str

class CategoryBase(BaseModel):
    category_id: int
    category_name: str

class ArticleBase(BaseModel):
    pk_article_id: int
    title: str
    body: str
    publish_date: date
    fk_author_id: int
    fk_category_id: int

#Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependence = Annotated[Session, Depends(get_db)]

#Получение пользователя
@app.get("/user/{id}")
async def get_user(id: Annotated[int, Path(title="ID пользователя", ge=0)], db: db_dependence):
    result = db.query(models.Author).filter(models.Author.author_id == id).first()
    error_404("user not found", result)
    return result

#Получение категории
@app.get("/category")
async def get_category(category_name: Annotated[str, Query(title="Название категории" ,min_length=2)], db: db_dependence):
    result = db.query(models.Category).filter(models.Category.category_name == category_name).first()
    error_404("category not found", result)
    return result

#Получение статьи
@app.get("/article/{id}")
async def get_article(id: Annotated[int, Path(title="ID статьи", ge=0)], db:db_dependence):
    result = db.query(models.Article).filter(models.Article.pk_article_id == id).first()
    error_404("article not found", result)
    return result

#Страница с регистрацией
@app.get("/registration")
async def registration(req: Request):
    return template.TemplateResponse(
        name="registration.html",
        context={"request": req}
    )

#Добавление пользователя
@app.post("/addUser")
async def add_user(author: AuthorBase, db: db_dependence):
    db_author = models.Author(
        first_name= author.first_name,
        last_name = author.last_name,
        middle_name = author.middle_name,
        birth_date = author.birth_date,
        author_login = author.author_login,
        author_password = hash_password(author.author_password, author.author_login)
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

#Добавление категории
@app.post("/addCategory")
async def add_category(category: CategoryBase, db: db_dependence):
    db_category=models.Category(
        category_id = category.category_id,
        category_name = category.category_name
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

#Добваление статьи
@app.post("/addArticle")
async def addArticle(article: ArticleBase, db: db_dependence):
    db_article = models.Article(
        pk_article_id = article.pk_article_id,
        title = article.title,
        body = article.body,
        publish_date = article.publish_date,
        fk_author_id = article.fk_author_id,
        fk_category_id = article.fk_category_id
    )
    db.add(db_article)
    db.commit()
    db.refresh((db_article))
