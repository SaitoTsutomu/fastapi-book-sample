import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_book_sample.database import Author, Base, Book, get_db
from fastapi_book_sample.main import app


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


@pytest.fixture(autouse=True)
def override_get_db(db):
    def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client_:
        yield client_


# ダミーデータ


async def add_author(db, author_data) -> dict:
    author = Author(**author_data, id=None, books=[])
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return {"id": author.id, "name": author.name}


async def add_book(db, book_data) -> dict:
    author = await db.get(Author, book_data["author_id"])
    book = Book(**book_data, id=None, author=author)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return {"id": book.id, "name": book.name, "author_id": book.author_id}


@pytest.fixture
def author1_data() -> dict:
    return {"name": "宮沢賢治"}


@pytest.fixture
def author2_data() -> dict:
    return {"name": "芥川龍之介"}


@pytest_asyncio.fixture
async def author1(db, author1_data) -> dict:
    return await add_author(db, author1_data)


@pytest_asyncio.fixture
async def author2(db, author2_data) -> dict:
    return await add_author(db, author2_data)


@pytest.fixture
def book1_data(author1) -> dict:
    return {"name": "銀河鉄道の夜", "author_id": author1["id"]}


@pytest_asyncio.fixture
async def book1(db, book1_data) -> dict:
    return await add_book(db, book1_data)
