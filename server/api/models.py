import uuid
from datetime import datetime
from hashlib import md5
from typing import Optional, List

from pydantic import BaseModel, validator, ValidationError

from core.db import mongo


# class Example(BaseModel):
#     name: str = None
#     signup_ts: Optional[datetime] = None
#     friends: List[int] = []


class Employees(BaseModel):
    last_name: str
    first_name: str = None
    middle_name: str = None
    role_id: str = None
    email: str = None
    age: int = 0
    phone_number: str = None
    iin: str = 0
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Category(BaseModel):
    title: str
    description: str = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Roles(BaseModel):
    title: str
    description: str = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Tariffs(BaseModel):
    title: str = None
    description: str = None
    role_id: str = None
    tariff: float = 0.0
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Tools(BaseModel):
    title: str = None
    description: str = None
    price: float = 0.0
    state: int = 0
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Sizes(BaseModel):
    title: str = None
    description: str = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Colors(BaseModel):
    title: str = None
    description: str = None
    key: str = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Brands(BaseModel):
    title: str = None
    description: str = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Expenses(BaseModel):
    title: str = None
    description: str = None
    sum: float = 0.0
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Goods(BaseModel):
    title: str
    description: str = None
    old_price: float = 0.0
    new_price: float = 0.0
    discount: float = 0.0
    attachments: List[str] = []
    rating: float = 0.0
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    sale_date: Optional[datetime] = None
    status: int = 0


class Applications(BaseModel):
    name: str
    email: str
    phone_number: str
    state: int = 0
    descriptions: str = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0


class Carts(BaseModel):
    status: int = 1


class Overheads(BaseModel):
    title: str
    description: str = None
    code: str
    datetime: Optional[datetime]
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int = 0

    @validator('code')
    def func_code(cls, v):
        if not v:
            return str(uuid.uuid4())

        return v
