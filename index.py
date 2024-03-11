from fastapi import FastAPI

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config.db import create_connection, create_cursor  # Import statements added
# import mysql.connector

app = FastAPI()

# Allow CORS for all origins for development purposes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request and response
class Student(BaseModel):
    name: str
    sex: str
    age: int
    phone: str
# deb connection calling 
db_conn = create_connection()
cursor = create_cursor(db_conn)
# index page
@app.get("/")
def read_index():
    return {'Well Come to FastAPI Training'}
# CRUD operations

    

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int):
    select_query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(select_query, (student_id,))
    student = cursor.fetchone()

    if student:
        return student

    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/students/", response_model=list[Student])
def read_students(skip: int = 0, limit: int = 10):
    select_query = "SELECT * FROM students LIMIT %s OFFSET %s"
    cursor.execute(select_query, (limit, skip))
    students = cursor.fetchall()

    return students

@app.post("/students/", response_model=Student)
def create_student(student: Student):
    insert_query = "INSERT INTO students (name, sex, age, phone) VALUES (%s, %s, %s, %s)"
    values = (student.name, student.sex, student.age, student.phone)

    cursor.execute(insert_query, values)
    db_conn.commit()

    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    update_query = "UPDATE students SET name=%s, sex=%s, age=%s, phone=%s WHERE id=%s"
    values = (updated_student.name, updated_student.sex, updated_student.age, updated_student.phone, student_id)

    cursor.execute(update_query, values)
    db_conn.commit()

    return updated_student

@app.patch("/students/{student_id}", response_model=Student)
def patch_student(student_id: int, patch_data: dict):
    # Assuming patch_data is a dictionary containing the fields to be updated
    # Example patch_data: {"name": "Updated Name", "age": 25}

    # Check if the student exists
    select_query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(select_query, (student_id,))
    existing_student = cursor.fetchone()

    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Apply the patch updates
    updated_data = {**existing_student, **patch_data}

    # Update the database
    update_query = (
        "UPDATE students SET name=%s, sex=%s, age=%s, phone=%s WHERE id=%s"
    )
    values = (
        updated_data["name"],
        updated_data["sex"],
        updated_data["age"],
        updated_data["phone"],
        student_id,
    )

    cursor.execute(update_query, values)
    db_conn.commit()

    return updated_data

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    delete_query = "DELETE FROM students WHERE id=%s"
    cursor.execute(delete_query, (student_id,))
    db_conn.commit()

    return JSONResponse(content={"message": "Student deleted successfully"}, status_code=200)


