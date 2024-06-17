import pytest
from app.db import get_user, create_user, delete_user, get_feedback, create_feedback, delete_feedback, cur

def test_get_user_not_found():
    user_id = get_user('notfound@test.com')
    assert user_id is None

def test_get_user_found():
    delete_user('john@example.com')
    expected = create_user('John Smith', 'john@example.com', '123456789')
    actual = get_user('john@example.com')
    assert expected == actual

def test_get_feedback_not_found():
    ans = get_feedback(9, "model")
    assert ans is None

def test_get_feedback_found():
    delete_feedback(1, "gpt-3.5-turbo")
    create_feedback(1, 5, "some rationale")
    ans = get_feedback(1, "gpt-3.5-turbo")
    assert ans == (5, 'some rationale') 

def test_feedback():
    ans = cur.execute("select * from feedbacks where id=7;").fetchall()
    assert ans is None

