from fastapi import FastAPI
import mysql.connector
from fastapi.encoders import jsonable_encoder
# from enum import Enum
from datetime import date
from pydantic import BaseModel

app = FastAPI()

try:
    mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="learnmot"
    )
    print("Contect Successful")
except mysql.connector.Error as err:
    # Si se produce un error, imprime el mensaje de error
    print(f"Error: {err}")
finally:
    # Asegúrate de cerrar la conexión, independientemente de si se realizó con éxito o no.
    if 'conn' in locals():
        mydb.close()

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
    teacher_id: int
    student_id: int
    topic: str 
    description: str 
    since_date: date 
    until_date: date

class Observation(BaseModel):
    description: str
    academic_load_id: int 

@app.get("/")
def root():
    return {"message": "My FastApi"}

# CRUD USERS
@app.get("/list/users")
def list_users():
    try:
        db = mydb.cursor()
        db.execute("SELECT * FROM users")
        response = db.fetchall()
        payload = []
        content = {} 
        for item in response:
            content={
                'id':item[0],
                'name':item[1],
                'last_name':item[2],
                'sex':item[3],
                'role':item[4],
                'email':item[5],
                'password':item[6],
            }
            payload.append(content)
            content = {}
        print(payload)
        json_data = jsonable_encoder(payload)            
        return {"result": json_data}
    except Exception as error:
        return {"error":error}

@app.post("/insert/user")
def insert_user(newuser: User):
    try:
        name = newuser.name
        last_name = newuser.last_name
        sex = newuser.sex
        role = newuser.role
        email = newuser.email
        password = newuser.password
        db = mydb.cursor() 
        db.execute("""
                   INSERT INTO users(name,last_name,sex,role,email,password) VALUES(%s,%s,%s,%s,%s,%s)""",
                   (name,last_name,sex,role,email,password))
        mydb.commit()
        db.close()
        return {"info":"User create successfully."}
    except Exception as error:
        return {"error":error}

@app.put("/update/user/{id}")
def update_user(id: int, updateuser: User):
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


# CRUD Academic Load
@app.get("/list/academicload")
def list_academic_load():
    try:
        db = mydb.cursor()
        db.execute("SELECT * FROM academic_load")
        response = db.fetchall()
        payload = []
        content = {}
        for item in response:
            content = {
                "idTeacher": item[0],
                "idStudent": item[1],
                "topic": item[2],
                "description": item[3],
                "since_date": item[4],
                "until_date": item[5]
            }
            payload.append(content)
            content = {}
        json_data = jsonable_encoder(payload)
        return {"result": json_data}
    except Exception as error:
        return {"error": error}

@app.post("/insert/academicload")
def insert_academic_load(academic: AcademicLoad):
    try: 
        teacher_id = academic.teacher_id
        student_id = academic.student_id
        topic = academic.topic
        description = academic.description
        since_date = academic.since_date
        until_date = academic.until_date
        db = mydb.cursor()
        db.execute("""
                INSERT INTO academic_load 
                (teacher_id, student_id, topic, description, since_date, until_date)
                VALUES (%s,%s,%s,%s,%s,%s)
            """,(teacher_id, student_id, topic, description, since_date, until_date))
        mydb.commit()
        db.close()
        return {"info": "Academic load created successfully."}
    except Exception as error:
        return {"error":error}

@app.put("/update/academicload/{id}")
def update_academic_load(id: int, academic: AcademicLoad):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM academic_load WHERE id = %s"
        db.execute(idsql,(id,))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"Id '{id}' not found."}
        
        teacher_id = academic.teacher_id
        student_id = academic.student_id
        topic = academic.topic
        description = academic.description
        since_date = academic.since_date
        until_date = academic.until_date
        update = """
            UPDATE academic_load SET 
            teacher_id = %s,
            student_id = %s,
            topic = %s,
            description = %s,
            since_date = %s,
            until_date = %s
            WHERE id = %s
            """
        db.execute(update,(teacher_id, student_id, topic, description, since_date, until_date, id))
        mydb.commit()
        db.close()
        return {"info":"Academic load updated successfully."}
    except Exception as error:
        return {"result":error}

@app.delete("/delete/academicload/{id}")
def delete_academic_load(id: int):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM academic_load WHERE id = %s"
        db.execute(idsql,(id,))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"Id '{id}' not found."}
        delete = "DELETE FROM academic_load WHERE id = %s"
        db.execute(delete,(id,))
        mydb.commit()
        db.close()
        return {"info": "Academic load removed successfully."}
    except Exception as error:
        return {"error": error}


#CRUD observation
@app.get("/list/observation")
def list_observation():
    try:
        db = mydb.cursor()
        db.execute("SELECT * FROM observation")
        response = db.fetchall()
        payload = []
        content = {}
        for item in response:
            content = {
                'academic_load_id': item[0],
                'observation_desc': item[1]
            }
            payload.append(content)
            content = {}
        json_data = jsonable_encoder(payload)
        return {"result": json_data}
    except Exception as error:
        return {"error":error}
    
@app.post("/insert/observation")
def insert_observation(observation: Observation):
    try:
        description = observation.description
        academic_load_id = observation.academic_load_id
        db = mydb.cursor()
        db.execute("""
                INSERT INTO observation (description, academic_load_id)
                VALUES (%s,%s)
            """,(description, academic_load_id))
        mydb.commit()
        db.close()
        return {"info": "New Observation is created successfully."}
    except Exception as error:
        return {"result":error}

# @app.put("/update/observation")


#  --------------------------------------------------------------
# delete method using clause "like"+
@app.delete("/deletelike/users/{name}")
def deletelike(name: str):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM users WHERE name LIKE %s"
        db.execute(idsql,(f"%{name}%",))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"No value was found '{name}'"}
        namesql = ("DELETE FROM users WHERE name LIKE %s")
        db.execute(namesql,(f"%{name}%",))
        mydb.commit()
        db.close()
        return {"info": f"User '{name}' removed successful."}
    except Exception as error:
        return {"result":error}

# get method using clause "sum"
@app.get("/users/count")
def userscount():
    try:
        db = mydb.cursor()
        count = "SELECT COUNT(*) FROM users"
        db.execute(count)
        result = db.fetchall()
        payload =  []
        content = {}
        for res in result:
            content={
                "count":res[0]
            }
            payload.append(content)
            content = {}
        db.close()
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
    
@app.get("/users/docente/academicload/{id}")
def get_teacher_by_subject(id: int):
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
        # payload = []
        # content = {} 
        # for res in result:
        #     content={
        #         'id':res[0],
        #         'name':res[1],
        #         'last_name':res[2],
        #         'role':res[3],
        #         'topic':res[4],
        #     }
        #     payload.append(content)
        #     content = {}
        # print(payload)
        json_data = jsonable_encoder(result)            
        return {"result": json_data}
    except (Exception) as error:
        return {"result":error}
    
@app.get("/users/subject/observation/{id}/{topic}")
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
