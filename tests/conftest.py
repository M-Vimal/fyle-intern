import pytest
import os
from tests import app
import json
from flask_migrate import upgrade

@pytest.fixture(autouse=True, scope="function")
def reset_database():
    """
    Delete the SQLite database file and run migrations to reset the schema.
    This fixture is automatically applied to each test function.
    """
    db_path = 'core/store.sqlite3'
    
    # Delete the database file if it exists
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except PermissionError:
        print(f"Could not remove {db_path}. It may be in use.")

    # Run migrations to initialize the database schema
    with app.app_context():
        upgrade(directory='core/migrations')  # Apply all migrations, creating tables as defined in your models

@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers
