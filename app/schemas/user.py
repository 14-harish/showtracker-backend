from pydantic import BaseModel, EmailStr

# what client SENDS
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# what client RECEIVES
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
