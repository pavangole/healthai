from optparse import Option
from typing import Optional

import uvicorn
from pydantic import BaseModel

from databases.database import Base

class Auth(BaseModel):
    email: str
    password: str
    name: str
    role: str
    class Config:
        orm_mode = True

class Docter(BaseModel):
    name: str
    docter_id: str
    class Config:
        orm_mode = True


class DocterInfo(BaseModel):
    speciality: str
    age: int
    clinic: str 
    class Config:
        orm_mode = True


class PatientInfo(BaseModel):
    age: int
    address: str

