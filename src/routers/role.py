from datetime import datetime, date
import hashlib
from operator import ge
from typing import Annotated, Optional
from fastapi import HTTPException, Path, APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from src.models import Role
from src.database import db_dependence
from src.errors import given_error
from src.routers.auth import get_current_user, oauth2_bearer
from src.hash_password import hash_password

router = APIRouter(prefix='/role', tags=['router ролей'])

class RoleBase(BaseModel):
    role_name: str

@router.post('/add')
async def add_role(role: RoleBase, db: db_dependence):
    db_role = Role(
        role_name = role.role_name
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)

@router.get('/get')
async def get_role(id: int ,db:db_dependence):
    db_role = db.query(Role).filter(Role.pk_role_id == id).first()
    given_error("Роль не найдена", db_role, 404)
    return db_role
