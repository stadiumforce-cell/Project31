# backend/models.py

from datetime import date


class Member:
    def __init__(self, member_id, name, address, phone, email, age, profession, active=True):
        self.member_id = member_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.age = age
        self.profession = profession
        self.active = active

    def __str__(self):
        return f"{self.member_id} | {self.name} | {self.email}"


class Book:
    def __init__(self, book_id, title, author, category, isbn, stock, total_loans=0):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.isbn = isbn
        self.stock = stock
        self.total_loans = total_loans

    def __str__(self):
        return f"{self.book_id} | {self.title} | {self.author}"


class Loan:
    def __init__(self, loan_id, member_id, book_id, loan_date, return_date=None, status="active", rating=None):
        self.loan_id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.status = status  # active / returned
        self.rating = rating  # 1–5 or None

    def __str__(self):
        return f"{self.loan_id} | Member {self.member_id} | Book {self.book_id} | {self.status}"
