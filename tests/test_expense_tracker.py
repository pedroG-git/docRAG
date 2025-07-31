import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from expense_tracker import (
    create_user,
    create_group,
    add_expense,
    get_group_balances,
)


def test_balances():
    u1 = create_user('Alice', 'alice@example.com')
    u2 = create_user('Bob', 'bob@example.com')
    g = create_group('Trip', [u1.id, u2.id])
    add_expense(g.id, 'Hotel', 100, u1.id, {u1.id: 50, u2.id: 50})
    balances = get_group_balances(g.id)
    assert balances[u1.id] == 50  # Alice paid 100 but owes 50 -> +50
    assert balances[u2.id] == -50
