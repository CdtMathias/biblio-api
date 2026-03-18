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

def test_get_member():
    token = get_token()
    response = client.get("/members", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_member_by_id():
    token = get_token()
    create_response = client.post("/members", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "name": "Oui",
        "tel": "3",
    })
    member_id = create_response.json()["id"]
    response = client.get(f"/members/{member_id}", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

def test_get_member_not_found():
    token = get_token()
    response = client.get("/members/999", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404

# POST #

def test_create_member():
    token = get_token()
    response = client.post("/members", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "name": "Testeur",
        "tel": "3",
    })
    assert response.status_code == 200

def test_create_member_invalid():
    token = get_token()
    response = client.post("/members", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "name": "Testeurjuwdbiuewfebfwubwubefoiw",
        "tel": "3",
    })
    assert response.status_code == 422


