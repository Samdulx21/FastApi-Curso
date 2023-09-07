from fastapi import FastAPI
# import mysql.connector
# from fastapi.encoders import jsonable_encoder
import modelsClass

app = FastAPI()

# mydb = mysql.connector.connect(
#   host = "localhost",
#   user = "root",
#   password = "",
#   database  = ""
# )


@app.get("/")
def root():
    return {"message": "hello sam"}
