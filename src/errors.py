from fastapi import HTTPException, status
from src.routers.auth import get_current_user
from src.models import Role, Author

def given_error(error_text: str, object_to_check: bool, status: int):
    if not object_to_check:
        raise HTTPException(status_code=status, detail=error_text)
    
async def get_author_requst_from(token, db):
    user:dict = await get_current_user(token)
    db_author_requst_from = db.query(Author).filter(user.get('id') == Author.author_id).first()
    return db_author_requst_from
#Проверка роли пользователя
async def error_forbidden_admin_only(token, db):
    db_author_requst_from = await get_author_requst_from(token, db)
    if db_author_requst_from.fk_role != db.query(Role).filter(Role.role_name == "Администратор").first().pk_role_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='У вас нет прав для этой команды')

async def error_forbidden_admin_and_user(token, db, db_author):
    db_author_requst_from = await get_author_requst_from(token, db)
    if db_author_requst_from.fk_role != db.query(Role).filter(Role.role_name == "Администратор").first().pk_role_id and db_author_requst_from.author_id != db_author.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='У вас нет прав для этой команды')
