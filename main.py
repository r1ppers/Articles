from datetime import date, datetime
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Path, Query, Body, Request
from typing import Annotated
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator
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

class AuthorBase(BaseModel):
    first_name: str = Field(..., description='Имя пользователя от 1 до 50 символов', min_length=1, max_length=50)
    last_name: str = Field(..., description='Фамилия пользователя от 1 до 50 символов', min_length=1, max_length=50)
    middle_name: str = Field(description='Отчество пользователя от 1 до 50 символов', min_length=0, max_length=50)
    birth_date: date = Field(..., description='Дата рождения пользователя')
    author_login: str = Field(..., description='Логин пользователя', min_length=1, max_length=50)
    author_email: str = Field(..., description='Электронная почта пользователя')
    author_password: str = Field(..., description='Пароль пользователя', min_length=1, max_length=50)

    #Указание корректной даты рождения
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, birth_date: date):
        if birth_date.year >= datetime.now().date().year:
            raise HTTPException(status_code=406, detail="Дата рождения должна быть меньше текущего года")
        return birth_date


class CategoryBase(BaseModel):
    category_name: str = Field(..., description='Название категории', min_length=1, max_length=50)

class ArticleBase(BaseModel):
    title: str = Field(..., description='Название статьи', min_length=1, max_length=50)
    body: str = Field(..., description='Текст статьи', max_length=50000)
    publish_date: date = Field(..., description='Дата публикации')
    fk_author_id: int = Field(..., description='Идентификатор пользователя (Внешний ключ)')
    fk_category_id: int = Field(..., description='Идентификатор категории (Внешний ключ)')

#Создание таблиц в БД
#models.Base.metadata.create_all(bind=engine)

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

#Добавление пользователя
@app.post("/addUser")
async def add_user(author: AuthorBase, db: db_dependence):
    db_author = models.Author(
        first_name = author.first_name,
        last_name = author.last_name,
        middle_name = author.middle_name,
        birth_date = author.birth_date,
        author_login = author.author_login,
        author_email = author.author_email,
        author_password = hash_password(author.author_password, author.author_login)
    )
    author.validate_birth_date(author.birth_date)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

#Добавление категории
@app.post("/addCategory")
async def add_category(category: CategoryBase, db: db_dependence):
    db_category=models.Category(
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
        title = article.title,
        body = article.body,
        publish_date = article.publish_date,
        fk_author_id = article.fk_author_id,
        fk_category_id = article.fk_category_id
    )
    db.add(db_article)
    db.commit()
    db.refresh((db_article))
