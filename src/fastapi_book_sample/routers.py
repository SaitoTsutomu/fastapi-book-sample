from typing import Annotated

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


@router.post("/authors", tags=["/authors"])
async def add_author(author: AuthorAdd, db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorGet:
    return await functions.add_author(db, **author.model_dump())


@router.post("/books", tags=["/books"])
async def add_book(book: BookAdd, db: Annotated[AsyncSession, Depends(get_db)]) -> BookGet:
    book_new = await functions.add_book(db, **book.model_dump())
    if book_new is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return book_new


@router.get("/authors", tags=["/authors"])
async def get_authors(db: Annotated[AsyncSession, Depends(get_db)]) -> list[AuthorGet]:
    return await functions.get_authors(db)


@router.get("/books", tags=["/books"])
async def get_books(db: Annotated[AsyncSession, Depends(get_db)]) -> list[BookGet]:
    return await functions.get_books(db)


@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorGet:
    author = await functions.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return author


@router.get("/books/{book_id}", tags=["/books"])
async def get_book(book_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> BookGet:
    book = await functions.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return book


@router.get("/authors/{author_id}/details", tags=["/authors"])
async def author_details(author_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorGetWithBooks:
    author = await functions.author_details(db, author_id=author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return author


@router.get("/books/{book_id}/details", tags=["/books"])
async def book_details(book_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> BookGetWithAuthor:
    book = await functions.book_details(db, book_id=book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return book


@router.patch("/authors", tags=["/authors"])
async def update_author(author: AuthorUpdate, db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorGet:
    author_cur = await functions.update_author(db, **author.model_dump())
    if author_cur is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author.id")
    return author_cur


@router.patch("/books", tags=["/books"])
async def update_book(book: BookUpdate, db: Annotated[AsyncSession, Depends(get_db)]) -> BookGet:
    book_cur = await functions.update_book(db, **book.model_dump())
    if book_cur is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book.id or book.author_id")
    return book_cur


@router.delete("/authors", tags=["/authors"])
async def delete_author(author_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
    ok = await functions.delete_author(db, author_id=author_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")


@router.delete("/books", tags=["/books"])
async def delete_book(book_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
    ok = await functions.delete_book(db, book_id=book_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
