from collections.abc import AsyncIterator

import sqlalchemy.orm
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class Author(sqlalchemy.orm.MappedAsDataclass, Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(16))
    books: Mapped[list["Book"]] = relationship(
        "Book", back_populates="author", cascade="all, delete"
    )


class Book(sqlalchemy.orm.MappedAsDataclass, Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(Author)


engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3", echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        authors = await session.scalars(select(Author))
        if not authors.first():
            author1 = Author(id=None, name="夏目漱石", books=[])
            author2 = Author(id=None, name="泉鏡花", books=[])
            book1 = Book(id=None, name="坊っちゃん", author_id=None, author=author1)
            book2 = Book(id=None, name="高野聖", author_id=None, author=author2)
            session.add_all([author1, author2, book1, book2])
            await session.commit()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(engine) as session:
        yield session
