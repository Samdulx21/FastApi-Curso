from fastapi import FastAPI
# import mysql.connector
# from fastapi.encoders import jsonable_encoder
from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# mydb = mysql.connector.connect(
#   host = "localhost",
#   user = "root",
#   password = "",
#   database  = ""
# )

# class SelectRole(str, Enum):
#     Admin = 'admin'
#     Teacher = 'teacher'
#     Student = 'student'

# class Sex(str, Enum):
#     Male = 'male'
#     Female = 'female' 

class Users(BaseModel):
    name: str = Field(min_length=1, max_length=10)
    last_name: str = Field(min_length=1, max_length=10)
    role: str 
    sex: str
    email: str
    password: str = Field(min_length=1, max_length=10)

class Rol(BaseModel):
    name: str = Field(min_length=1, max_length=25   )
    description: str = Field(min_length=1, max_length=25)

class Attribute(BaseModel):
    name: str 
    description: str

class Subject(BaseModel):
    name: str = Field(min_length=1, max_length=10)
    name_code: str = Field(min_length=1, max_length=10, gt=1, lt=11)
    description: str = Field(min_length=1, max_length=200)

class Module(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    descripion: str = Field(min_length=1, max_length=25)

class AcademicLoad(BaseModel):
    topic: str = Field(min_length=1, max_length=15)
    description: str = Field(min_length=1, max_length=200)
    since_date: date 
    until_date: date

class Observation(BaseModel):
    Observations: str = Field(max_legth=600)

@app.get("/")
def root():
    return {"message": "hello sam"}
