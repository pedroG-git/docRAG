from typing import Dict, List
from pydantic import BaseModel

# In-memory stores
_users: Dict[int, "User"] = {}
_groups: Dict[int, "Group"] = {}
_expenses: List["Expense"] = []

# Simple incrementing IDs
def _next_id(store: Dict[int, BaseModel]) -> int:
    return max(store.keys(), default=0) + 1

class User(BaseModel):
    id: int
    name: str
    email: str

class Group(BaseModel):
    id: int
    name: str
    members: List[int]

class Expense(BaseModel):
    id: int
    group_id: int
    description: str
    amount: float
    paid_by: int
    splits: Dict[int, float]  # user_id -> amount owed

# CRUD functions

def create_user(name: str, email: str) -> User:
    user_id = _next_id(_users)
    user = User(id=user_id, name=name, email=email)
    _users[user_id] = user
    return user


def create_group(name: str, member_ids: List[int]) -> Group:
    group_id = _next_id(_groups)
    group = Group(id=group_id, name=name, members=member_ids)
    _groups[group_id] = group
    return group


def add_expense(group_id: int, description: str, amount: float, paid_by: int, splits: Dict[int, float]) -> Expense:
    expense_id = len(_expenses) + 1
    expense = Expense(
        id=expense_id,
        group_id=group_id,
        description=description,
        amount=amount,
        paid_by=paid_by,
        splits=splits,
    )
    _expenses.append(expense)
    return expense


def get_group_balances(group_id: int) -> Dict[int, float]:
    balances: Dict[int, float] = {}
    for exp in _expenses:
        if exp.group_id != group_id:
            continue
        # payer contribution
        balances[exp.paid_by] = balances.get(exp.paid_by, 0) + exp.amount
        # subtract owed amounts
        for uid, amt in exp.splits.items():
            balances[uid] = balances.get(uid, 0) - amt
    return balances
