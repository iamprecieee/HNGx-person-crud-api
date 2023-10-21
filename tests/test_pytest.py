import pytest, json
from app import create_app
from resources.db import db

@pytest.fixture
def app():
    app = create_app("sqlite:///test_data.db")  # Use a standard test database
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_person(client):
    # Test creating a new person
    response = client.post(
        "/api",
        json={"name": "John Doe"}
    )
    assert response.status_code == 200
    assert json.loads(response.data.decode("utf-8")) == "Person created successfully."

def test_create_duplicate_person(client):
    # Test creating a person with a duplicate name (should fail)
    client.post(
        "/api",
        json={"name": "Jane Smith"}
    )
    response = client.post(
        "/api",
        json={"name": "Jane Smith"}
    )
    assert response.status_code == 400
    assert json.loads(response.data.decode("utf-8"))["description"] == "A person with that name already exists!"

def test_get_person(client):
    # Test retrieving a person by ID
    response_create = client.post(
        "/api",
        json={"name": "Jane Smith"}
    )
    response_get = client.get("/api/1")
    assert response_get.status_code == 200
    assert json.loads(response_get.data.decode("utf-8"))["name"] == "Jane Smith"

def test_get_person_by_name(client):
    # Test retrieving a person by name
    response_create = client.post(
        "/api",
        json={"name": "John Doe"}
    )
    response_get = client.get("/api/John%20Doe")  # Name with spaces
    assert response_get.status_code == 200
    assert json.loads(response_get.data.decode("utf-8"))["name"] == "John Doe"

def test_get_nonexistent_person(client):
    # Test retrieving a person that doesn't exist
    response = client.get("/api/9999")  # ID that doesn't exist
    assert response.status_code == 404
    assert json.loads(response.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."

def test_update_person(client):
    # Test updating a person's name
    response_create = client.post(
        "/api",
        json={"name": "Jane Smith"}
    )
    response_update = client.put("/api/1", json={"name": "Jane Doe"})
    assert response_update.status_code == 200
    assert json.loads(response_update.data.decode("utf-8"))["name"] == "Jane Doe"
    
def test_update_person_by_name(client):
    # Test updating a person by name
    response_create = client.post(
        "/api",
        json={"name": "Jane Smith"}
    )
    response_update = client.put("/api/Jane%20Smith", json={"name": "Jane Doe"})
    assert response_update.status_code == 200
    assert json.loads(response_update.data.decode("utf-8"))["name"] == "Jane Doe"

def test_delete_person(client):
    # Test deleting a person
    response_create = client.post(
        "/api",
        json={"name": "John Doe"}
    )
    response_delete = client.delete("/api/1")
    assert response_delete.status_code == 204
    assert not response_delete.data
    
def test_delete_person_by_name(client):
    # Test deleting a person by name
    response_create = client.post(
        "/api",
        json={"name": "John Doe"}
    )
    response_delete = client.delete("/api/John%20Doe")  # Name with spaces
    assert response_delete.status_code == 204
    assert not response_delete.data

def test_delete_nonexistent_person(client):
    # Test deleting a person that doesn't exist
    response_delete = client.delete("/api/9999")  # ID that doesn't exist
    assert response_delete.status_code == 404
    assert json.loads(response_delete.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
