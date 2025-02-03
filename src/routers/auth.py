from datetime import timedelta, datetime
from typing_extensions import deprecated
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from src.models import Author
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from src.database import db_dependence
from src.routers.author import hash_password

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '143fdohj8h87439psk0390k0fjhd9840ejgfdj0e94jpdf0'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class AuthorLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependence):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.author_login, user.author_id, timedelta(minutes=15))
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
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login:str = payload.get('sub')
        author_id: int = payload.get('id')
        if login is None or author_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не получилось определить пользователя.')
        return {'login': login, 'id': author_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не получилось определить пользователя.')
