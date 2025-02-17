from pydantic import BaseModel, EmailStr

class UserCreate (BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    email: EmailStr
    username: str



class UserLogin (BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id: int | None = None