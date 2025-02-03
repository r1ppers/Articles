from datetime import date
from turtle import title
from typing import Annotated
from fastapi import HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from src.models import Article
from src.database import db_dependence
from src.errors import given_error

router = APIRouter(prefix='/article', tags=['router для статей'])

class ArticleBase(BaseModel):
    title: str = Field(..., description='Название статьи', min_length=1, max_length=50)
    body: str = Field(..., description='Текст статьи', max_length=50000)
    publish_date: date = Field(..., description='Дата публикации')
    fk_author_id: int = Field(..., description='Идентификатор пользователя (Внешний ключ)')
    fk_category_id: int = Field(..., description='Идентификатор категории (Внешний ключ)')

#Получение статьи
@router.get("/get/{id}")
async def get_article(id: Annotated[int, Path(title="ID статьи", ge=0)], db:db_dependence):
    result = db.query(Article).filter(Article.pk_article_id == id).first()
    given_error("article not found", result, 404)
    return result

#Добавление статьи
@router.post("/add")
async def addArticle(article: ArticleBase, db: db_dependence):
    db_article = Article(
        title = article.title,
        body = article.body,
        publish_date = article.publish_date,
        fk_author_id = article.fk_author_id,
        fk_category_id = article.fk_category_id
    )
    db.add(db_article)
    db.commit()
    db.refresh((db_article))

@router.put('/update/{id}')
async def update_article(id: Annotated[int, Path(title='id статьи', ge=0)], article: ArticleBase, db: db_dependence):
    db_article = db.query(Article).filter(Article.pk_article_id == id).first()
    given_error('Статья не найдена', db_article, 404)

    db_article.title = article.title
    db_article.body = article.body
    db_article.publish_date = article.publish_date

    db.commit()
    db.refresh(db_article)

    return db_article

@router.delete('/delete/{id}')
async def delete_article(id: Annotated[int, Path(title="id статьи", ge=0)], db: db_dependence):
    db_article = db.query(Article).filter(Article.pk_article_id == id).first()
    given_error('Статья не найдена', db_article, 404)
    db.delete(db_article)
    db.commit()

    return {'Сообщение': 'Статья удалена'}