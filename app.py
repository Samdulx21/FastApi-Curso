from fastapi import FastAPI
import mysql.connector
from fastapi.encoders import jsonable_encoder
# from enum import Enum
from datetime import date
from pydantic import BaseModel

app = FastAPI()

# mydb = mysql.connector.connect(
#   host = "localhost",
#   user = "root",
#   password = "",
#   database  = ""
# )
try:
    mydb = mysql.connector.connect(
        host="172.17.0.3",
        port=3306,
        user="root",
        password="secret",
        database="learnmot"
    )
    print("conexion exitosa")
except mysql.connector.Error as err:
    # Si se produce un error, imprime el mensaje de error
    print(f"Error de conexión a la base de datos: {err}")

finally:
    # Asegúrate de cerrar la conexión, independientemente de si se realizó con éxito o no.
    if 'conn' in locals():
        mydb.close()


# class SelectRole(str, Enum):
#     Admin = 'admin'


# class Sex(str, Enum):
#     Male = 'male'
#     Female = 'female' 
#     Female = 'female'

class Users(BaseModel):
    name: str 
    last_name: str 
    role: str 
    name: str
    last_name: str
    sex: str
    role: str
    email: str
    password: str 
    password: str


class Rol(BaseModel):
    name: str 
    description: str 
    name: str
    description: str


class Attribute(BaseModel):
    name: str 
    name: str
    description: str


class Subject(BaseModel):
    name: str 
    name_code: str 
    description: str 
    name: str
    name_code: str
    description: str


class Module(BaseModel):
    name: str 
    descripion: str 
    name: str
    descripion: str


class AcademicLoad(BaseModel):
    topic: str 
    description: str 
    since_date: date 
    topic: str
    description: str
    since_date: date
    until_date: date


class Observation(BaseModel):
    Observations: str 
    Observations: str


@app.post("/insertarusers")
def insertarusers(newUsers: Users):
    try:
        name = newUsers.name
        last_name = newUsers.last_name
        sex = newUsers.sex
        role = newUsers.role
        email = newUsers.email
        password = newUsers.password
        insertar = mydb.cursor()
        insertar.execute("INSERT INTO users (name,last_name,sex,role,email,password)VALUES(%s,%s,%s,%s,%s,%s)",
                         (name, last_name, sex, role, email, password))
        mydb.commit()
        insertar.close()
        return {"informacion": "empleado registrado"}
    except Exception as error:
        print(f"Error al insertar en la base de datos: {error}")


@app.get("/listausers")
def listausers():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        payload = []
        content = {}
        for data in result:
            content = {
                'id': data[0],
                'name': data[1],
                'last_name': data[2],
                'sex': data[3],
                'role': data[4],
                'email': data[5],
                'password': data[6]
            }
            payload.append(content)
            content = {}
        print(payload)   
        json_data = jsonable_encoder(payload)
        return {"resultado": json_data}
    except (Exception) as error:
        return {"resultado": error}
@app.put("/update/user/{id}")
def update_user(id: int, updateuser: Users):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM users WHERE id = %s"
        db.execute(idsql,(id,))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"Id '{id}' not found."}
        name = updateuser.name
        last_name = updateuser.last_name
        sex = updateuser.sex
        role = updateuser.role
        email = updateuser.email
        password = updateuser.password
        update = """
            UPDATE users SET
            name = %s,
            last_name = %s,
            sex = %s,
            role = %s,
            email = %s,
            password = %s
            WHERE id = %s
        """
        db.execute(update,(name,last_name,sex,role,email,password, id))
        mydb.commit()
        db.close()
        return {"info":"User updated successfully."}
    except Exception as error:    
        return {"error":error}
@app.delete("/delete/user/{id}")
def delete_user(id: int):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM users WHERE id = %s"
        db.execute(idsql, (id,))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"Id '{id}' not found."}
        delete = "DELETE FROM users WHERE id = %s"
        db.execute(delete, (id,))
        mydb.commit()
        db.close()
        return {"infor":"User deleted successfully."}
    except Exception as error:
        return {"result":error}


@app.delete("/deletelike/users/{name}")
def deletelike(name: str):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM users WHERE name LIKE %s", (name,))
        mydb.commit()
        cursor.close()
        return {"info": "User removed successful."}
    except Exception as error:
        return {"result": error}


@app.get("/userscount/users")
def userscount():
    try:
        data = mydb.cursor()
        data.execute("SELECT COUNT(role) FROM users")
        result = data.fetchall()
        payload = []
        content = {}
        for res in result:
            content = {
                'role': res[0],
                #'name':res[1],
                # 'las_name':res[2],
                # 'sex':res[3],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)
        return {"result": json_data}
    except Exception as error:
        return {"result": error}

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
        """, (id,))
        result = data.fetchall()
        payload = []
        content = {}
        for res in result:
            content = {
                'id': res[0],
                'name': res[1],
                'last_name': res[2],
                'role': res[3],
                'topic': res[4],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)
        return {"result": json_data}
    except (Exception) as error:
        return {"result": error}


@app.get("/")
def root():
    return {"message": "hello sam"}
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
        """, (id, topic,))
        result = data.fetchall()
        payload = []
        content = {}
        for res in result:
            content = {
                'id': res[0],
                'name': res[1],
                'last_name': res[2],
                'role': res[3],
                'topic': res[4],
                'observation_desc': res[5],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)
        return {"result": json_data}
    except (Exception) as error:
        return {"result": error}