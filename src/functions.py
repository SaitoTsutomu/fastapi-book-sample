from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import Author, Book


async def add_author(db: AsyncSession, *, name: str) -> Author:
    author_new = Author(id=None, name=name, books=[])
    db.add(author_new)
    await db.commit()
    await db.refresh(author_new)
    return author_new


async def add_book(db: AsyncSession, *, name: str, author_id: int) -> Book | None:
    author = await get_author(db, author_id=author_id)
    if not author:
        return None
    book_new = Book(id=None, name=name, author_id=author.id, author=author)
    db.add(book_new)
    await db.commit()
    await db.refresh(book_new)
    return book_new


async def get_authors(db: AsyncSession) -> ScalarResult:
    return await db.scalars(select(Author))


async def get_books(db: AsyncSession) -> ScalarResult:
    return await db.scalars(select(Book))


async def get_author(db: AsyncSession, *, author_id: int) -> Author | None:
    return await db.get(Author, author_id)


async def get_book(db: AsyncSession, *, book_id: int) -> Book | None:
    return await db.get(Book, book_id)


async def author_details(db: AsyncSession, *, author_id: int) -> Author | None:
    return await db.scalar(
        select(Author).where(Author.id == author_id).options(selectinload(Author.books))
    )


async def book_details(db: AsyncSession, *, book_id: int) -> Book | None:
    return await db.scalar(
        select(Book).where(Book.id == book_id).options(selectinload(Book.author))
    )


async def update_author(db: AsyncSession, *, id: int, name: str | None) -> Author | None:
    author_cur = await db.get(Author, id)
    if not author_cur:
        return None
    if name is not None:
        author_cur.name = name
    await db.commit()
    await db.refresh(author_cur)
    return author_cur


async def update_book(
    db: AsyncSession, *, id: int, name: str | None, author_id: int | None
) -> Book | None:
    book_cur = await db.get(Book, id)
    if not book_cur:
        return None
    if name is not None:
        book_cur.name = name
    if author_id is not None:
        author_cur = await db.get(Author, author_id)
        if not author_cur:
            return None
        book_cur.author = author_cur
    await db.commit()
    await db.refresh(book_cur)
    return book_cur


async def delete_author(db: AsyncSession, *, author_id: int) -> bool:
    author = await db.get(Author, author_id)
    if author is None:
        return False
    await db.delete(author)
    await db.commit()
    return True


async def delete_book(db: AsyncSession, *, book_id: int) -> bool:
    book = await db.get(Book, book_id)
    if book is None:
        return False
    await db.delete(book)
    await db.commit()
    return True
