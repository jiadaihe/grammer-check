import pytest
from app.db import get_user

def test_get_user_not_found():
    user_id = get_user('notfound@test.com')
    assert user_id is None

def test_get_user_found():
    user_id = get_user('notfound@example.com')
    assert user_id is None
