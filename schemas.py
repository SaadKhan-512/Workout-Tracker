from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class User_Create(BaseModel):
    email: EmailStr
    password: str

# Schema for token data
class Token_Data(BaseModel):
    id: Optional[int] = None