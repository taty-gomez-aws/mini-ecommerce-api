from pydantic import BaseModel, EmailStr


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
