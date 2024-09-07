import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_book_sample.database import Author, Base, Book, get_db
from fastapi_book_sample.main import app
from fastapi_book_sample.schemas import AuthorGet, BookGet


@pytest_asyncio.fixture
async def engine():
    engine_ = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine_.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine_
    await engine_.dispose()


@pytest_asyncio.fixture
async def db(engine):
    async with AsyncSession(engine) as db_:
        yield db_


@pytest_asyncio.fixture(autouse=True)
async def override_get_db(db):
    async def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client_:
        yield client_


# ダミーデータ


async def add_author(db, author_data):
    author = Author(**author_data, id=None, books=[])
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return AuthorGet.model_validate(author).model_dump()


async def add_book(db, book_data):
    author = await db.get(Author, book_data["author_id"])
    book = Book(**book_data, id=None, author=author)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return BookGet.model_validate(book).model_dump()


@pytest_asyncio.fixture
async def author1_data():
    return {"name": "宮沢賢治"}


@pytest_asyncio.fixture
async def author2_data():
    return {"name": "芥川龍之介"}


@pytest_asyncio.fixture
async def author1(db, author1_data):
    return await add_author(db, author1_data)


@pytest_asyncio.fixture
async def author2(db, author2_data):
    return await add_author(db, author2_data)


@pytest_asyncio.fixture
async def book1_data(author1):
    return {"name": "銀河鉄道の夜", "author_id": author1["id"]}


@pytest_asyncio.fixture
async def book1(db, book1_data):
    return await add_book(db, book1_data)
