from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped
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
