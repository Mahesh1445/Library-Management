from fastapi import FastAPI  # Corrected import statement
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["students_db"]
collection = db["students"]

# FastAPI setup
app = FastAPI()


class Address(BaseModel):
    city: str
    country: str


class Student(BaseModel):
    name: str
    age: int
    address: Address

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 20,
                "address": {
                    "city": "New York",
                    "country": "USA"
                }
            }
        }
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome To FastAPI World"}

@app.post("/students", response_model=dict)
async def create_student(student: Student):
    student_dict = student.dict()
    result = collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}


@app.get("/students", response_model=List[Student])
async def list_students(country: Optional[str] = Query(None), age: Optional[int] = Query(None)):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students = collection.find(query)
    return list(students)


@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.patch("/students/{student_id}", response_model=dict)
async def update_student(student_id: str, student: Student):
    student_dict = student.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(student_id)}, {"$set": student_dict})
    if result.modified_count == 1:
        return {"message": "Student updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{student_id}", response_model=dict)
async def delete_student(student_id: str):
    result = collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
