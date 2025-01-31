from datetime import datetime, date
from os import error
from typing import Annotated
from fastapi import HTTPException, Path, APIRouter, Query
from pydantic import BaseModel, Field, field_validator
from models import Category
from database import db_dependence
from errors import given_error

router = APIRouter()

class CategoryBase(BaseModel):
    category_name: str = Field(..., description='Название категории', min_length=1, max_length=50)

#Получение категории
@router.get("/category")
async def get_category(category_name: Annotated[str, Query(title="Название категории" ,min_length=2)], db: db_dependence):
    result = db.query(Category).filter(Category.category_name == category_name).first()
    given_error("category not found", result, 404)
    return result

#Добавление категории
@router.post("/addCategory")
async def add_category(category: CategoryBase, db: db_dependence):
    db_category=Category(
        category_name = category.category_name
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

