from datetime import datetime, date
from typing import Annotated
from fastapi import HTTPException, Path, APIRouter, Depends
from pydantic import BaseModel, Field, field_validator
from src.models import Author
from src.database import db_dependence
from src.errors import given_error, error_forbidden_admin_only, error_forbidden_admin_and_user
from src.routers.auth import oauth2_bearer
from src.hash_password import hash_password

router = APIRouter(prefix='/author', tags=['router для автора'])

class AuthorBase(BaseModel):
    first_name: str = Field(..., description='Имя пользователя от 1 до 50 символов', min_length=1, max_length=50)
    last_name: str = Field(..., description='Фамилия пользователя от 1 до 50 символов', min_length=1, max_length=50)
    middle_name: str = Field(None, description='Отчество пользователя от 1 до 50 символов', min_length=0, max_length=50)
    birth_date: date = Field(..., description='Дата рождения пользователя')
    author_login: str = Field(..., description='Логин пользователя', min_length=1, max_length=50)
    author_email: str = Field(..., description='Электронная почта пользователя')
    author_password: str = Field(..., description='Пароль пользователя', min_length=1, max_length=50)
    fk_role_id: int = Field(..., description='Роль пользователя')

    #Указание корректной даты рождения
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, birth_date: date):
        if birth_date.year >= datetime.now().date().year:
            raise HTTPException(status_code=406, detail="Дата рождения должна быть меньше текущего года")
        return birth_date

#Получение пользователя
@router.get("/get/{id}")
async def get_user(id: Annotated[int, Path(title="ID пользователя", ge=0)], db: db_dependence):
    result = db.query(Author).filter(Author.author_id == id).first()
    given_error("user not found", result, 404)
    return result

#Добавление пользователя
@router.post("/add")
async def add_user(author: AuthorBase, db: db_dependence):
    db_author = Author(
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

@router.put("/Update/{id}")
async def put_author(id: Annotated[int, Path(title="id пользователя")], author: AuthorBase, db: db_dependence):
    db_author = db.query(Author).filter(Author.author_id == id).first()
    given_error("Пользователь не найден", db_author, 404)

    db_author.first_name = author.first_name
    db_author.last_name = author.last_name
    db_author.middle_name = author.middle_name
    db_author.birth_date = author.birth_date
    db_author.author_login = author.author_login
    db_author.author_email = author.author_email
    
    # Проверяем валидность даты рождения
    author.validate_birth_date(author.birth_date)
    
    # Сохраняем изменения в базе данных
    db.commit()
    db.refresh(db_author)
    
    return db_author

@router.put("/updateRole/{id}")
async def update_role(id: Annotated[int, Path(title='id пользователя')], id_role: int, token: Annotated[str, Depends(oauth2_bearer)], db: db_dependence):
    db_author = db.query(Author).filter(Author.author_id == id).first()
    given_error("Пользователь не найден", db_author, 404)
    await error_forbidden_admin_only(token, db)
    db_author.fk_role = id_role
    db.commit()
    db.refresh(db_author)

    return db_author


@router.put("/updatePassword/{id}")
async def update_password(id: Annotated[int, Path(title="Id пользователя", ge=0)], old_password: str, new_password: str ,db: db_dependence):
    db_author = db.query(Author).filter(Author.author_id == id).first()
    given_error("Пользователь не найден", db_author, 404)
    if hash_password(old_password, db_author.author_login) != db_author.author_password:
        raise HTTPException(status_code=400, detail="Неправильный пароль")
    db_author.author_password = hash_password(new_password, db_author.author_login)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.delete('/delete/{id}')
async def delete_user(id: Annotated[int, Path(title="Id пользователя", ge=0)], token: Annotated[str, Depends(oauth2_bearer)], db: db_dependence):
    db_author = db.query(Author).filter(Author.author_id == id).first()
    given_error("Пользователь не найден", db_author, 404)
    #Проверка пользователь сам удаляет свой профиль или является ли пользователь, от которого исходит запрос, администратором 
    await error_forbidden_admin_and_user(token, db, db_author)
    db.delete(db_author)
    db.commit()
    return {'Сообщение': "Пользователь удален"}
