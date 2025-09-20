from fastapi import FastAPI, Depends, status, Query, Path, HTTPException
from sqlalchemy.orm import Session

from crud import (
    get_all_authors,
    get_author_by_name,
    get_author_by_id,
    add_author_to_db,
    get_all_books, add_book_to_db
)
from database import SessionLocal
from schemas import AuthorRead, AuthorCreate, BookRead, BookCreate

app = FastAPI()

def get_db() -> Session:  # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/authors", response_model=list[AuthorRead])
def list_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(3, ge=1, le=100),
        db: Session = Depends(get_db)
):
    return get_all_authors(db=db, skip=skip, limit=limit)

@app.post("/authors", response_model=AuthorRead)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = get_author_by_name(db=db, author_name=author.name)
    if db_author is None:
        db_author = add_author_to_db(author=author, db=db)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Author already exists"
    )

@app.get("/authors/{author_id}", response_model=AuthorRead)
def get_author(author_id: int = Path(ge=1), db: Session = Depends(get_db)):
    db_author = get_author_by_id(db=db, author_id=author_id)
    if db_author:
        return db_author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Author not found"
    )

@app.get("/books", response_model=list[BookRead])
def list_books(
        author_id: int = Query(None, ge=1),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    return get_all_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )

@app.post("/books", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return add_book_to_db(book=book, db=db)