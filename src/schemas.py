from pydantic import BaseModel as BaseModel_
from pydantic import ConfigDict


class BaseModel(BaseModel_):
    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str


class Author(AuthorBase):
    id: int | None = None


class AuthorAdd(AuthorBase):
    pass


class AuthorGet(AuthorAdd):
    id: int


class AuthorGetWithBooks(AuthorGet):
    books: list["BookGet"]


class AuthorUpdate(BaseModel):
    id: int
    name: str | None = None


class BookBase(BaseModel):
    name: str
    author_id: int | None = None


class Book(BookBase):
    id: int | None = None


class BookAdd(BookBase):
    author_id: int


class BookGet(BookAdd):
    id: int


class BookGetWithAuthor(BookGet):
    author: AuthorGet


class BookUpdate(BaseModel):
    id: int
    name: str | None = None
    author_id: int | None = None
