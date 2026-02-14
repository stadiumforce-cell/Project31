# backend/storage_txt.py

from backend.models import Member, Book, Loan
from datetime import datetime


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def parse_date(value):
    if value == "None" or value == "":
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def format_date(value):
    return value.strftime("%Y-%m-%d") if value else "None"


# ---------------------------------------------------------
# LOAD FUNCTIONS
# ---------------------------------------------------------

def load_members_from_txt(path):
    members = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 9:
                    continue

                member = Member(
                    member_id=int(parts[0]),
                    name=parts[1],
                    address=parts[2],
                    phone=parts[3],
                    email=parts[4],
                    age=int(parts[5]),
                    profession=parts[6],
                    gender=parts[7],
                    active=(parts[8] == "True")
                )
                members[member.member_id] = member
    except FileNotFoundError:
        pass

    return members


def load_books_from_txt(path):
    books = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 7:
                    continue

                book = Book(
                    book_id=int(parts[0]),
                    title=parts[1],
                    author=parts[2],
                    category=parts[3],
                    isbn=parts[4],
                    stock=int(parts[5]),
                    total_loans=int(parts[6])
                )
                books[book.book_id] = book
    except FileNotFoundError:
        pass

    return books


def load_loans_from_txt(path):
    loans = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 7:
                    continue

                loan = Loan(
                    loan_id=int(parts[0]),
                    member_id=int(parts[1]),
                    book_id=int(parts[2]),
                    loan_date=parse_date(parts[3]),
                    return_date=parse_date(parts[4]),
                    status=parts[5],
                    rating=None if parts[6] == "None" else int(parts[6])
                )
                loans[loan.loan_id] = loan
    except FileNotFoundError:
        pass

    return loans


# ---------------------------------------------------------
# SAVE FUNCTIONS
# ---------------------------------------------------------

def save_members_to_txt(path, members):
    with open(path, "w", encoding="utf-8") as f:
        for m in members.values():
            f.write(
                f"{m.member_id}|{m.name}|{m.address}|{m.phone}|{m.email}|"
                f"{m.age}|{m.profession}|{m.gender}|{m.active}\n"
            )


def save_books_to_txt(path, books):
    with open(path, "w", encoding="utf-8") as f:
        for b in books.values():
            f.write(
                f"{b.book_id}|{b.title}|{b.author}|{b.category}|{b.isbn}|"
                f"{b.stock}|{b.total_loans}\n"
            )


def save_loans_to_txt(path, loans):
    with open(path, "w", encoding="utf-8") as f:
        for l in loans.values():
            f.write(
                f"{l.loan_id}|{l.member_id}|{l.book_id}|"
                f"{format_date(l.loan_date)}|{format_date(l.return_date)}|"
                f"{l.status}|{l.rating}\n"
            )
