import re
from sqlalchemy import ForeignKey, false
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.database import Base


class Author(Base):
    __tablename__ = 'author'
    author_id: Mapped[int] = mapped_column(primary_key=True, index = True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str]= mapped_column()
    middle_name: Mapped[str]= mapped_column()
    birth_date: Mapped[date]= mapped_column()
    author_login: Mapped[str] = mapped_column()
    author_email: Mapped[str] = mapped_column()
    author_password: Mapped[str]= mapped_column()
    #default = 1, под номером один находится обычный пользователь
    fk_role: Mapped[int] = mapped_column(ForeignKey('user_role.pk_role_id'), default=1, nullable=False)

    #Установка каскадного удаления для связанных объектов
    articles = relationship("Article", back_populates="author", cascade="all, delete")

class Category(Base):
    __tablename__ = 'category'
    category_id: Mapped[int]= mapped_column(primary_key=True, index = True, autoincrement=True)
    category_name: Mapped[str] = mapped_column()

class Article(Base):
    __tablename__ = 'article'
    pk_article_id:Mapped[int] = mapped_column(primary_key=True, index = True, autoincrement=True)
    title: Mapped[str]= mapped_column()
    body: Mapped[str]= mapped_column()
    publish_date: Mapped[date]= mapped_column()
    fk_author_id: Mapped[int]= mapped_column(ForeignKey("author.author_id"))
    fk_category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))

    #Установка каскадного удаления для связанных объектов
    author = relationship("Author", back_populates="articles")

class Role(Base):
    __tablename__ = 'user_role'
    pk_role_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    role_name: Mapped[str]
