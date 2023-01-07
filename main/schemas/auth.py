from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {"example": {"username": "test_user", "password": "password"}}


class UserInCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    full_name: str
    username: str
    email: str
    hashed_password: str
    disabled: bool


class User(BaseModel):
    full_name: str
    email: str
    disabled: bool


class UserToken(BaseModel):
    token: str
