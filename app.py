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

@app.put("/updated/observation/{id}")
def update_observation(id: int, observation: Observation):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM observation WHERE id = %s"
        db.execute(idsql,(id,))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"Id '{id}' not found."}
        
        description = observation.description
        academic_load_id = observation.academic_load_id
        update = """
            UPDATE observation SET 
            description = %s,
            academic_load_id = %s
            WHERE id = %s
            """
        db.execute(update,(description,academic_load_id, id))
        mydb.commit()
        db.close()
        return {"info":"observation updated successfully."}
    except Exception as error:
        return {"result":error}

@app.delete("/delete/observation/{id}")
def delete_observation(id: int):
    try:
        db = mydb.cursor()
        idsql = "SELECT id FROM observation WHERE id = %s"
        db.execute(idsql,(id,))
        response = db.fetchone()
        if not response:
            db.close()
            return {"info": f"Id '{id}' not found."}
        delete = "DELETE FROM observation WHERE id = %s"
        db.execute(delete,(id,))
        mydb.commit()
        db.close()
        return {"info": "observation load removed successfully."}
    except Exception as error:
        return {"error": error}


#  --------------------------------------------------------------
# get method using inner joins on two tables and clausule where
@app.get("/filter/observation/academicload/{id}")
def get_observation_academicload(id: int):
    try:
        db = mydb.cursor()
        query = """
            SELECT o.description, al.topic
            FROM observation as o
            JOIN academic_load as al
            ON o.academic_load_id = al.id
            WHERE al.teacher_id = %s
        """
        db.execute(query, (id,))
        response = db.fetchall()
        db.close()
        return {"result": response}
    except Exception as error:
        return {"error":error}
    
@app.get("/filter/users/academicload/{id}")
def get_observation_academicload(id: int):
    try:
        db = mydb.cursor()
        query = """
            SELECT u.name, u.sex, al.topic
            FROM users as u
            JOIN academic_load as al
            ON u.id = al.student_id
            WHERE al.student_id = %s
        """
        db.execute(query, (id,))
        response = db.fetchall()
        db.close()
        return {"result": response}
    except Exception as error:
        return {"error":error}


# get method using inner joins on three tables
@app.get("/filter/users/academicload/observation/{id}")
def get_users_observation(id: int):
    try:
        db = mydb.cursor()
        query = """
            SELECT u.name, al.topic, o.description
            FROM users as u
            JOIN academic_load as al 
            ON u.id = al.student_id
            JOIN observation as o
            ON al.id = o.academic_load_id
            WHERE u.id = %s
        """
        db.execute(query,(id,))
        response = db.fetchall()
        db.close()
        return {"result":response}
    except Exception as error:
        return {"error":error}
    
@app.get("/filter/users/role/academicload/{id}")
def get_users_observation(id: int):
    try:
        db = mydb.cursor()
        query = """
            SELECT u.name, al.topic, r.description
            FROM users as u
            JOIN role_users as ru
            ON u.id = ru.user_id
            JOIN roles r
            ON ru.role_id = r.id
            JOIN academic_load as al 
            ON u.id = al.teacher_id
            WHERE u.id = %s
        """
        db.execute(query,(id,))
        response = db.fetchall()
        db.close()
        return {"result":response}
    except Exception as error:
        return {"error":error}


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

# get method using clause "count"
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


#get method using clause "sum"
@app.get("/subject/sum")
def subject_sum():
    try:
        db = mydb.cursor()
        sum = "SELECT SUM(price + iva) FROM subject"
        db.execute(sum)
        response = db.fetchall()
        payload =  []
        content = {}
        for res in response:
            content={
                "sum":res[0]
            }
            payload.append(content)
            content = {}
        db.close()
        json_data = jsonable_encoder(payload)            
        return {"result": json_data}
    except Exception as error:
        return {"result":error}
    

# get method using joins on two tables with clausule where and order by.
@app.get("/users/teacher/academicload/{id}")
def get_teacher_by_subject(id: int):
    try:
        db = mydb.cursor()
        db.execute("""
            SELECT u.id, u.name, u.last_name, al.topic
            FROM users as u 
            JOIN academic_load as al
            on u.id = al.teacher_id
            WHERE u.id = %s
            ORDER BY al.topic DESC 
        """,(id,))
        response = db.fetchall()
        db.close()       
        return {"result": response}
    except Exception as error:
        return {"result":error}
    
# get method using joins on three tables with clausule where, and o or.
@app.get("/users/al/observation/{id}/{topic}")
def get_users_academicload_observation(id: int, topic: str):
    try:
        db = mydb.cursor()
        query = """
            SELECT u.name, u.last_name, al.topic, o.description
            FROM users as u
            JOIN academic_load as al 
            ON u.id = al.student_id
            JOIN observation as o
            ON al.id = o.academic_load_id
            WHERE u.id = %s
            AND al.topic = %s
        """
        db.execute(query,(id,topic))
        response = db.fetchall()
        db.close()         
        return {"result": response}
    except Exception as error:
        return {"result":error}
