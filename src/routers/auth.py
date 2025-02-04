from datetime import timedelta, datetime
from typing_extensions import deprecated
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from starlette import status
from src.models import Author
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from src.database import db_dependence
from src.hash_password import hash_password

router = APIRouter(
    prefix='/auth',
    tags=['router для Вход/выход']
)

SECRET_KEY = '143fdohj8h87439psk0390k0fjhd9840ejgfdj0e94jpdf0'
ALGORITHM = 'HS256'

black_list_token = set()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class AuthorLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: db_dependence):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.author_login, user.author_id, timedelta(minutes=15))
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(login: str, password: str, db)-> Optional[Author]:
    author = db.query(Author).filter(Author.author_login == login).first()
    if not author:
        return False
    if hash_password(password, login) != author.author_password:
        return False
    return author 
    
def create_access_token(login: str, author_id: int, expires_delta: timedelta):
    encode = {'sub': login, 'id': author_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    if token in black_list_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен недействителен')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login:str = payload.get('sub')
        author_id: int = payload.get('id')
        if login is None or author_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не получилось определить пользователя.')
        return {'login': login, 'id': author_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не получилось определить пользователя.')

@router.get('/logout')
async def logout(token: Annotated[str, Depends(oauth2_bearer)], response:Response):
    black_list_token.add(token)
    response.delete_cookie(key="access_token")
    return {"Сообщение":"Выход из системы"}