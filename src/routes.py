# routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from functions import *
from expense_tracker import (
    create_user,
    create_group,
    add_expense,
    get_group_balances,
)

router = APIRouter()

class Query(BaseModel):  # Define a request body model
    text: str

@router.get("/docRAG/")
async def docRAG_endpoint(query: Query):  # Accept the Query model as a parameter
    return docRAG(query.text)


class UserIn(BaseModel):
    name: str
    email: str


@router.post("/users")
async def create_user_api(user: UserIn):
    return create_user(user.name, user.email)


class GroupIn(BaseModel):
    name: str
    members: List[int]


@router.post("/groups")
async def create_group_api(group: GroupIn):
    return create_group(group.name, group.members)


class ExpenseIn(BaseModel):
    description: str
    amount: float
    paid_by: int
    splits: Dict[int, float]


@router.post("/groups/{group_id}/expenses")
async def add_expense_api(group_id: int, expense: ExpenseIn):
    return add_expense(
        group_id,
        expense.description,
        expense.amount,
        expense.paid_by,
        expense.splits,
    )


@router.get("/groups/{group_id}/balances")
async def balances_api(group_id: int):
    return get_group_balances(group_id)

