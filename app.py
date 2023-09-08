from fastapi import FastAPI
import mysql.connector
from fastapi.encoders import jsonable_encoder
from enum import Enum
from datetime import date
from pydantic import BaseModel

app = FastAPI()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="learnmot"
)

# class SelectRole(str, Enum):
#     Admin = 'admin'
#     Teacher = 'teacher'
#     Student = 'student'

# class Sex(str, Enum):
#     Male = 'male'
#     Female = 'female' 

class User(BaseModel):
    name: str 
    last_name: str 
    sex: str
    role: str 
    email: str
    password: str 

class Role(BaseModel):
    name: str 
    description: str 

class Attribute(BaseModel):
    name: str 
    description: str

class Subject(BaseModel):
    name: str 
    name_code: str
    description: str 

class Module(BaseModel):
    name: str 
    descripion: str 

class AcademicLoad(BaseModel):
    topic: str 
    description: str 
    since_date: date 
    until_date: date

class Observation(BaseModel):
    Observations: str 

# {
#   "name": "samuel",
#   "last_name": "dulce",
#   "sex": "male",
#   "role": "estudiante",
#   "email": "samuel@gmail.com",
#   "password": "samuel123"
# }

@app.get("/")
def root():
    return {"message": "hello sam"}

@app.get("/listusers")
def listusers():
    try:
        data = mydb.data()
        data.execute("SELECT * FROM users")
        result = data.fetchall()
        payload = []
        content = {} 
        for res in result:
            content={
                'id':res[0],
                'name':res[1],
                'last_name':res[2],
                'sex':res[3],
                'role':res[4],
                'email':res[5],
                'password':res[6],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)            
        return {"result": json_data}
    except (Exception) as error:
        return {"error":error}

@app.post("/insertuser")
def insertuser(newuser: User):
    try:
        name = newuser.name
        last_name = newuser.last_name
        sex = newuser.sex
        role = newuser.role
        email = newuser.email
        password = newuser.password
        data = mydb.data() 
        data.execute("INSERT INTO users(name,last_name,sex,role,email,password) VALUES(%s,%s,%s,%s,%s,%s)",(name,last_name,sex,role,email,password))
        mydb.commit()
        data.close()
        return {"info":"User create successful."}
    except Exception as error:
        return {"error":error}

@app.delete("users/deletelike/{name}")
def deletelike(name: str):
    try:
        data = mydb.data()
        data.execute("DELETE FROM users WHERE name like = '%s'",(name,))
        mydb.commit()
        data.close()
        return {"info":"User removed successful."}
    except Exception as error:
        return {"result":error}

@app.get("users/userscount")
def userscount():
    try:
        data = mydb.data()
        data.execute("SELECT COUNT(role) FROM users")
        result = data.fetchall()
        payload = []
        content = {}
        for res in result:
            content={
                'role':res[0],
                # 'name':res[1],
                # 'las_name':res[2],
                # 'sex':res[3],
            }
        payload.append(content)
        content = {}
        print(payload)
        json_data = jsonable_encoder(payload)            
        return {"result": json_data}
    except Exception as error:
        return {"result":error}
    
# @app.get("users/usersum")
# def usersum():
#     try:
#         data = mydb.data()
#         data.execute("SELECT SUM(role) FROM subject")
#         result = data.fetchall()
#         payload = []
#         content = {}
#         for res in result:
#             content={
#                 'role':res[0],
#                 # 'name':res[1],
#                 # 'las_name':res[2],
#                 # 'sex':res[3],
#             }
#         payload.append(content)
#         content = {}
#         print(payload)
#         json_data = jsonable_encoder(payload)            
#         return {"resultado": json_data}
#     except Exception as error:
#         return {"resultado":error}
    
@app.get("users/docente/subject/{id}")
def getTeacherBySubject(id: int):
    try:
        data = mydb.data()
        data.execute("""
            SELECT u.id, u.name, u.last_name, u.role, al.topic
            FROM academic_load al
            JOIN users u 
            on u.id = al.teacher_id
            WHERE al.id = %s
            ORDER BY al.topic DESC 
        """,(id,))
        result = data.fetchall()
        payload = []
        content = {} 
        for res in result:
            content={
                'id':res[0],
                'name':res[1],
                'last_name':res[2],
                'role':res[3],
                'topic':res[4],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)            
        return {"result": json_data}
    except (Exception) as error:
        return {"result":error}
    
@app.get("users/subject/observation/{id}/{topic}")
def getSubjectAndObservation(id: int, topic: str):
    try:
        data = mydb.data()
        data.execute("""
            SELECT u.id, u.name, u.last_name, u.role, al.topic, o.observation_desc
            FROM academic_load al
            JOIN users u 
            on al.teacher_id = u.id
            JOIN observation o 
            on o.academic_load_id = al.id
            WHERE al.id = %s
            AND al.topic = %s
        """,(id, topic,))
        result = data.fetchall()
        payload = []
        content = {} 
        for res in result:
            content={
                'id':res[0],
                'name':res[1],
                'last_name':res[2],
                'role':res[3],
                'topic':res[4],
                'observation_desc':res[5],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)            
        return {"result": json_data}
    except (Exception) as error:
        return {"result":error}
