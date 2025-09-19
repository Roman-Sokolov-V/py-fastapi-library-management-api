from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ---------------- Book ----------------
class BookBase(BaseModel):
    title: str
    publication_date: datetime
    author_id: int

class BookCreate(BookBase):
    summary: str

class BookTitle(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)

class BookRead(BookBase):
    id: int
    summary: str
    model_config = ConfigDict(from_attributes=True)

# ---------------- Author ----------------
class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class AuthorList(AuthorBase):
    id: int
    books: list[BookTitle]  # список книг без рекурсії
    model_config = ConfigDict(from_attributes=True)