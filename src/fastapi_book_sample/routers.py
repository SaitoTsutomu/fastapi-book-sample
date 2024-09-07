from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import functions
from .database import get_db
from .schemas import (
    AuthorAdd,
    AuthorGet,
    AuthorGetWithBooks,
    AuthorUpdate,
    BookAdd,
    BookGet,
    BookGetWithAuthor,
    BookUpdate,
)

router = APIRouter()


@router.post("/authors", response_model=AuthorGet, tags=["/authors"])
async def add_author(author: AuthorAdd, db: AsyncSession = Depends(get_db)):
    return await functions.add_author(db, **author.model_dump())


@router.post("/books", response_model=BookGet, tags=["/books"])
async def add_book(book: BookAdd, db: AsyncSession = Depends(get_db)):
    book_new = await functions.add_book(db, **book.model_dump())
    if book_new is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return book_new


@router.get("/authors", response_model=list[AuthorGet], tags=["/authors"])
async def get_authors(db: AsyncSession = Depends(get_db)):
    return await functions.get_authors(db)


@router.get("/books", response_model=list[BookGet], tags=["/books"])
async def get_books(db: AsyncSession = Depends(get_db)):
    return await functions.get_books(db)


@router.get("/authors/{author_id}", response_model=AuthorGet, tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await functions.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return author


@router.get("/books/{book_id}", response_model=BookGet, tags=["/books"])
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await functions.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return book


@router.get("/authors/{author_id}/details", response_model=AuthorGetWithBooks, tags=["/authors"])
async def author_details(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await functions.author_details(db, author_id=author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return author


@router.get("/books/{book_id}/details", response_model=BookGetWithAuthor, tags=["/books"])
async def book_details(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await functions.book_details(db, book_id=book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return book


@router.patch("/authors", response_model=AuthorGet, tags=["/authors"])
async def update_author(author: AuthorUpdate, db: AsyncSession = Depends(get_db)):
    author_cur = await functions.update_author(db, **author.model_dump())
    if author_cur is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author.id")
    return author_cur


@router.patch("/books", response_model=BookGet, tags=["/books"])
async def update_book(book: BookUpdate, db: AsyncSession = Depends(get_db)):
    book_cur = await functions.update_book(db, **book.model_dump())
    if book_cur is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book.id or book.author_id")
    return book_cur


@router.delete("/authors", response_model=None, tags=["/authors"])
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    ok = await functions.delete_author(db, author_id=author_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")


@router.delete("/books", response_model=None, tags=["/books"])
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    ok = await functions.delete_book(db, book_id=book_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
