from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from auth import hash_password, verify_password, create_token, verify_token
from database import load_books, get_book_by_id, get_book_by_state, add_book, update_book, update_state_book, delete_book, load_members, get_member_by_id, add_member, update_member, delete_member, load_loans, get_loan_by_id, update_loan, create_loan, delete_loan, return_loan, create_user, get_user

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "My biblio API"}

# BOOKS #

class BookSchema(BaseModel):
    title: str = Field(min_length=1, max_length=40)
    author: str = Field(min_length=1, max_length=20)
    year_published: str = Field(min_length=1, max_length=5)
    state: str = Field(default="available")

@app.get("/books")
def get_all_books(payload = Depends(verify_token)):
    books = load_books()
    return [book.to_dict() for book in books]

@app.get("/books/{id}")
def get_books_by_id(id: int, payload = Depends(verify_token)):
    result = get_book_by_id(id)
    if result:
        return result.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Book unfindable")

@app.get("/books/search/{state}")
def get_books_by_state(state: str, payload = Depends(verify_token)):
    results = get_book_by_state(state)
    if results:
        return [result.to_dict() for result in results]
    
@app.post("/books")
def create_books(book: BookSchema, payload = Depends(verify_token)):
    book_id = add_book(book.title, book.author, book.year_published)
    return {"id": book_id, "title": book.title, "author": book.author, "year_published": book.year_published}

@app.put("/books/{id}")
def update_books(id: int, book: BookSchema, payload = Depends(verify_token)):
    result = get_book_by_id(id)
    if result:
        update_book(id, book.title, book.author, book.year_published, book.state)
        return {"message": "Book updated"}
    else:
        raise HTTPException(status_code=404, detail="Book unfindable")

@app.delete("/books/{id}")
def delete_book(id):
    result = get_book_by_id(id)
    if result:
        delete_book(id)
        return {"message": "Book deleted"}
    else:
        raise HTTPException(status_code=404, detail="Book unfindable")

# MEMBER #

class MemberSchema(BaseModel):
    name: str = Field(min_length= 1, max_length=10)
    tel: str = Field(min_length=1, max_length=20)

@app.get("/members")
def get_all_members(payload = Depends(verify_token)):
    members = load_members()
    return [member.to_dict() for member in members]

@app.get("/members/{id}")
def get_members_by_id(id: int, payload = Depends(verify_token)):
    result = get_member_by_id(id)
    if result:
        return result.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Member unfindable")

@app.post("/members")
def post_members(member: MemberSchema, payload = Depends(verify_token)):
    member_id = add_member(member.name, member.tel)
    return {"id": member_id, "name": member.name, "tel": member.tel}

@app.put("/members/{id}")
def update_members_by_id(id: int, member: MemberSchema, payload = Depends(verify_token)):
    result = get_member_by_id(id)
    if result:
        update_member(id, member.name, member.tel)
        return {"message": "Member updated"}
    else:
        raise HTTPException(status_code=404, detail="Member unfindable")
    
@app.delete("/members/{id}")
def delete_members_by_id(id: int, payload = Depends(verify_token)):
    result = get_member_by_id(id)
    if result:
        delete_member(id)
        return {"message": "Member deleted"}
    else:
        raise HTTPException(status_code=404, detail="Member unfindable")
    
# LOANS #

class LoanSchema(BaseModel):
    member_id: int = Field(gt=0)
    book_id: int = Field(gt=0)
    date: datetime
    return_date: datetime
    is_returned: bool = Field(default = False)

@app.get("/loans")
def get_all_loans(payload = Depends(verify_token)):
    loans = load_loans()
    return [loan.to_dict() for loan in loans]

@app.get("/loans/rented")
def get_all_loans_rented(payload = Depends(verify_token)):
    loans = load_loans()
    for loan in loans:
        result = loan.to_dict()
        book = get_books_by_id(result["book_id"])
        member = get_members_by_id(result["member_id"])
        for loan in loans:
            if not result["is_returned"]:
                return {"message": f"{member["name"]} rentend {book["title"]} on {result["date"]} to return before {result["return_date"]}"}
        else:
            {"message": "No books rented"}

@app.get("/loans/{id}")
def get_loans_by_id(id: int, payload = Depends(verify_token)):
    result = get_loan_by_id(id)
    if result:
        return result.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Loan unfindable")

@app.post("/loans")
def post_loans(loan: LoanSchema, payload = Depends(verify_token)):
    is_book = get_book_by_id(loan.book_id)
    is_member = get_member_by_id(loan.member_id)
    print(f"is_book: {is_book}")
    print(f"is_member: {is_member}")
    print(f"is_book.state: {is_book.state if is_book else 'None'}")
    if is_book and is_member and is_book.state == "available":
        loan_id = create_loan(loan.member_id, loan.book_id, loan.date, loan.return_date)
        update_state_book(loan.book_id, "rented")
        return {"id": loan_id, "member_id": loan.member_id, "book_id": loan.book_id, "date": loan.date, "return_date": loan.return_date}
    elif is_book and is_book.state == "rented":
        raise HTTPException(status_code=409, detail="Book already rented")
    else:
        raise HTTPException(status_code=404, detail="Book or Member unfindable")
    
@app.put("/loans/{id}")
def update_loan_by_id(id: int, loan: LoanSchema, payload = Depends(verify_token)):
    result = get_loan_by_id(id)
    if result:
        update_loan(id, loan.member_id, loan.book_id, loan.date, loan.return_date)
        return {"message": "Loan updated"}
    else:
        raise HTTPException(status_code=404, detail="Loan unfindable")

@app.put("/loans/return/{id}")
def return_loan_by_id(id: int, payload = Depends(verify_token)):
    result = get_loan_by_id(id)
    if result:
        return_loan(id)
        update_state_book(result.book_id, "available")
        return {"message": "Book returned"}
    else:
        raise HTTPException(status_code=404, detail="Loan unfindable")
    
@app.delete("/loans/{id}")
def delete_loans_by_id(id: int, payload = Depends(verify_token)):
    result = get_loan_by_id(id)
    if result:
        delete_loan(id)
        return {"message": "Loan deleted"}
    else:
        raise HTTPException(status_code=404, detail="Loan unfindable")
    
# USER #

class UserSchema(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=20)

@app.post("/register")
def register(user: UserSchema):
    try:
        hashed_password = hash_password(user.password)
        create_user(user.username, hashed_password)
        return {"message": "Account created"}
    except Exception:
        raise HTTPException(status_code=409, detail="Username already exists")

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = get_user(form_data.username)
    if not user_data:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not verify_password(form_data.password, user_data[2]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": create_token({"sub": form_data.username}), "token_type": "bearer"}
