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

def test_get_loan():
    token = get_token()
    response = client.get("/loans", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_loan_by_id():
    token = get_token()
    create_member = client.post("/members", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "name": "TestId2",
        "tel": "3",
    })
    member_id = create_member.json()["id"]
    create_book = client.post("/books", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "title": "TestId2",
        "author": "Mathias",
        "year_published": "2000"
    })
    book_id = create_book.json()["id"]
    create_loan = client.post("/loans", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "member_id": member_id,
        "book_id": book_id,
        "date": "2026-03-18T11:04:14.901Z",
        "return_date": "2026-03-21T11:04:14.901Z",
    })
    loan_id = create_loan.json()["id"]
    response = client.get(f"/loans/{loan_id}", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

def test_get_loan_not_found():
    token = get_token()
    response = client.get("/loans/999", headers = {
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404

# POST #

def test_create_loan():
    token = get_token()
    create_member = client.post("/members", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "name": "TestLoan2",
        "tel": "3",
    })
    member_id = create_member.json()["id"]
    create_book = client.post("/books", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "title": "TestLoan2",
        "author": "Mathias",
        "year_published": "2000"
    })
    book_id = create_book.json()["id"]
    response = client.post("/loans", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "member_id": member_id,
        "book_id": book_id,
        "date": "2026-03-18T11:04:14.901Z",
        "return_date": "2026-03-21T11:04:14.901Z",
    })
    assert response.status_code == 200

def test_create_loan_invalid_id():
    token = get_token()
    response = client.post("/loans", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "member_id": "999",
        "book_id": "999",
        "date": "2026-03-18T11:04:14.901Z",
        "return_date": "2026-03-21T11:04:14.901Z",
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Book or Member unfindable"

def test_create_loan_invalid_already_rented():
    token = get_token()
    create_member = client.post("/members", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "name": "TestRent",
        "tel": "3",
    })
    member_id = create_member.json()["id"]
    create_book = client.post("/books", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "title": "TestRent",
        "author": "Mathias",
        "year_published": "2000"
    })
    book_id = create_book.json()["id"]
    first_loan = client.post("/loans", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "member_id": member_id,
        "book_id": book_id,
        "date": "2026-03-18T11:04:14.901Z",
        "return_date": "2026-03-21T11:04:14.901Z",
    })
    response = client.post("/loans", headers = {
        "Authorization": f"Bearer {token}"
    }, 
    json = {
        "member_id": member_id,
        "book_id": book_id,
        "date": "2026-03-18T11:04:14.901Z",
        "return_date": "2026-03-21T11:04:14.901Z",
    })
    assert first_loan.status_code == 200
    assert response.status_code == 409
    assert response.json()["detail"] == "Book already rented"


