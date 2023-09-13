from fastapi import FastAPI, Depends, HTTPException
import time
from typing import List
import services, database, models, schemas
from database import db_state_default

database.db.connect()
database.db.create_tables([models.Student])
database.db.close()

app = FastAPI()

sleep_time = 10

async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()

def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_student/", response_model = schemas.Student, dependencies=[Depends(get_db)])
def create_student(student: schemas.StudentCreate):
    db_student = services.get_student_by_email(email = student.email)
    if(db_student):
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_student(student = student)


@app.get("/get_student/{student_id}", response_model=schemas.Student, dependencies = [Depends(get_db)])
def get_student_by_id(student_id: int):
    db_student = services.get_student_by_id(student_id = student_id)
    if db_student is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return db_student

@app.get("/get_students/", response_model = List[schemas.Student], dependencies = [Depends(get_db)])
def read_students(skip: int = 0, limit: int = 10):
    students = services.get_students(skip=skip, limit=limit)
    return students

