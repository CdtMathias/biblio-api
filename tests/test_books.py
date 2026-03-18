from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    response = client.post("/login", data = {
        "username": "test123",
        "password": "test123"
    })
    return response.json()["access_token"]

# GET #

def test_get_book():
    token = get_token()
    response = client.get("/books", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book_by_id():
    token = get_token()
    create_response = client.post("/books", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "title": "Oui",
        "author": "Mathias",
        "year_published": "2000"
    })
    book_id = create_response.json()["id"]
    response = client.get(f"/books/{book_id}", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

def test_get_contact_not_found():
    token = get_token()
    response = client.get("/books/999", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404

# POST #

def test_create_book():
    token = get_token()
    response = client.post("/books", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "title": "BookTest",
        "author": "Mathias",
        "year_published": "2000"
    })
    assert response.status_code == 200

def test_create_book_invalid():
    token = get_token()
    response = client.post("/books", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "title": "BookTest",
        "author": "Mathias",
        "year_published": "2000jjbuubii"
    })
    assert response.status_code == 422



