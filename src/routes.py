# routes.py
from fastapi import APIRouter, Depends
from functions import *
from pydantic import BaseModel

router = APIRouter()

class Query(BaseModel):  # Define a request body model
    text: str

@router.get("/docRAG/")
async def docRAG_endpoint(query: Query):  # Accept the Query model as a parameter
    return docRAG(query.text)

