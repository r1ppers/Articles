from operator import ge
from typing import Annotated
from anyio import Path
from fastapi import APIRouter, Query, Path, Depends
from pydantic import BaseModel, Field, field_validator
from src.models import Category
from src.database import db_dependence
from src.errors import given_error, error_forbidden_admin_only
from src.routers.auth import oauth2_bearer

router = APIRouter(prefix='/category', tags=['router для категорий'])

class CategoryBase(BaseModel):
    category_name: str = Field(..., description='Название категории', min_length=1, max_length=50)

#Получение категории
@router.get("/get")
async def get_category(category_name: Annotated[str, Query(title="Название категории" ,min_length=2)], db: db_dependence):
    result = db.query(Category).filter(Category.category_name == category_name).first()
    given_error("category not found", result, 404)
    return result

#Добавление категории
@router.post("/add")
async def add_category(category: CategoryBase, token: Annotated[str, Depends(oauth2_bearer)], db: db_dependence):
    await error_forbidden_admin_only(token, db)
    db_category=Category(
        category_name = category.category_name
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/update/{id}")
async def update_category(id: Annotated[int, Path(title="id категории", ge=0)], category: CategoryBase, token: Annotated[str, Depends(oauth2_bearer)], db:db_dependence):
    db_category = db.query(Category).filter(Category.category_id == id).first()
    given_error("Категория не найдена", db_category, 404)
    await error_forbidden_admin_only(token, db)
    db_category.category_name = category.category_name

    db.commit()
    db.refresh(db_category)

    return db_category

@router.delete("/delete/{id}")
async def delete_category(id: Annotated[int, Path(title='id категории', ge=0)], token: Annotated[str, Depends(oauth2_bearer)], db: db_dependence):
    db_category = db.query(Category).filter(Category.category_id == id).first()
    given_error("Категория не найдена", db_category, 404)
    await error_forbidden_admin_only(token, db)
    db.delete(db_category)
    db.commit()

    return {'Сообщение': 'Категория удалена'}