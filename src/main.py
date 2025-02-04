from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from src.routers import author, article, category, auth, role
from src.database import db_dependence
from starlette import status
from src.routers.auth import get_current_user

app = FastAPI()
app.include_router(author.router)
app.include_router(article.router)
app.include_router(category.router)
app.include_router(auth.router)
app.include_router(role.router)

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get('/', status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependence):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"User": user}
