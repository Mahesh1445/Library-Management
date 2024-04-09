from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from pymongo import BaseModel

# MongoDB setup
client = BaseModel("mongodb://localhost:27017/")
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

