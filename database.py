import psycopg2
import os
from models.book_model import Book
from models.member_model import Member
from models.loan_model import Loan
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT")
)
cursor = conn.cursor()

# BOOKS #

def load_books():
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()

    return [Book(row[0], row[1], row[2], row[3], row[4]) for row in rows]

def get_book_by_id(id):
    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result:
        return Book(result[0], result[1], result[2], result[3], result[4])
    return None

def get_book_by_state(state):
    cursor.execute("SELECT * FROM books WHERE state = %s", (state,))
    rows = cursor.fetchall()

    return [Book(row[0], row[1], row[2], row[3], row[4]) for row in rows]

def add_book(title, author, year_published):
    try:
        cursor.execute("INSERT INTO books (title, author, year_published) VALUES (%s, %s, %s) RETURNING id", (title, author, year_published))
        conn.commit()
        return cursor.fetchone()[0]
    except Exception:
        conn.rollback()
        raise

def update_book(id,title, author, year_published, state):
    try:
        cursor.execute("UPDATE books SET title = %s, author = %s, year_published = %s, state = %s WHERE id = %s", (title, author, year_published, state, id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def update_state_book(id, state):
    try: 
        cursor.execute("UPDATE books SET state = %s WHERE id = %s", (state, id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def delete_book(id):
    try:
        cursor.execute("DELETE FROM books WHERE id = %s", (id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

# MEMBERS #

def load_members():
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    
    return [Member(row[0], row[1], row[2]) for row in rows]

def get_member_by_id(id):
    cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result:
        return Member(result[0], result[1], result[2])
    return None

def add_member(name, tel):
    try:
        cursor.execute("INSERT INTO members (name, tel) VALUES (%s, %s) RETURNING id", (name, tel))
        conn.commit()
        return cursor.fetchone()[0]
    except Exception:
        conn.rollback()
        raise

def update_member(id, name, tel):
    try:
        cursor.execute("UPDATE members SET name = %s, tel = %s WHERE id = %s", (name, tel, id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def delete_member(id):
    try:
        cursor.execute("DELETE FROM members WHERE id = %s", (id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

# LOANS #

def load_loans():
    cursor.execute("SELECT * FROM loans")
    rows = cursor.fetchall()
    return [Loan(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]

def get_loan_by_id(id):
    cursor.execute("SELECT * FROM loans WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result:
        return Loan(result[0], result[1], result[2], result[3], result[4], [5])
    return None

def create_loan(member_id, book_id, date, return_date):
    try:
        cursor.execute("INSERT INTO loans (member_id, book_id, date, return_date) VALUES (%s, %s, %s, %s) RETURNING id", (member_id, book_id, date, return_date))
        conn.commit()
        return cursor.fetchone()[0]
    except Exception:
        conn.rollback()
        raise    

def update_loan(id, member_id, book_id, date, return_date, is_returned):
    try: 
        cursor.execute("UPDATE loans SET member_id = %s, book_id = %s, date = %s, return_date = %s, is_returned = %s WHERE id = &s", (member_id, book_id, date, return_date, is_returned, id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def delete_loan(id):
    try:
        cursor.execute("DELETE FROM loans WHERE id = %s", (id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def return_loan(id):
    try:
        return_date = datetime.utcnow()
        cursor.execute("UPDATE loans SET return_date = %s, is_returned = True WHERE id = %s", (return_date, id))
    except Exception:
        conn.rollback()
        raise

# USER #

def create_user(username, hashed_password):
    try:
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

