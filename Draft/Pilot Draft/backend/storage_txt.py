# backend/storage_txt.py

from backend.models import Member, Book, Loan
from datetime import datetime


# ---------------------------------------------------------
# LOAD MEMBERS
# ---------------------------------------------------------
def load_members_from_txt(filename):
    members = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    continue  # skip invalid lines

                member_id = int(parts[0])
                name = parts[1]
                address = parts[2]
                phone = parts[3]
                email = parts[4]
                age = int(parts[5])
                profession = parts[6]

                members[member_id] = Member(
                    member_id, name, address, phone, email, age, profession
                )

    except FileNotFoundError:
        return {}

    return members


# ---------------------------------------------------------
# SAVE MEMBERS
# ---------------------------------------------------------
def save_members_to_txt(filename, members):
    with open(filename, "w", encoding="utf-8") as f:
        for m in members.values():
            f.write(
                f"{m.member_id}|{m.name}|{m.address}|{m.phone}|{m.email}|{m.age}|{m.profession}\n"
            )


# ---------------------------------------------------------
# LOAD BOOKS
# ---------------------------------------------------------
def load_books_from_txt(filename):
    books = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    continue

                book_id = int(parts[0])
                title = parts[1]
                author = parts[2]
                category = parts[3]
                isbn = parts[4]
                stock = int(parts[5])
                total_loans = int(parts[6])

                books[book_id] = Book(
                    book_id, title, author, category, isbn, stock, total_loans
                )

    except FileNotFoundError:
        return {}

    return books


# ---------------------------------------------------------
# SAVE BOOKS
# ---------------------------------------------------------
def save_books_to_txt(filename, books):
    with open(filename, "w", encoding="utf-8") as f:
        for b in books.values():
            f.write(
                f"{b.book_id}|{b.title}|{b.author}|{b.category}|{b.isbn}|{b.stock}|{b.total_loans}\n"
            )


# ---------------------------------------------------------
# LOAD LOANS
# ---------------------------------------------------------
def load_loans_from_txt(filename):
    loans = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    continue

                loan_id = int(parts[0])
                member_id = int(parts[1])
                book_id = int(parts[2])
                loan_date = datetime.strptime(parts[3], "%Y-%m-%d").date()

                return_date = (
                    datetime.strptime(parts[4], "%Y-%m-%d").date()
                    if parts[4] != "None"
                    else None
                )

                status = parts[5]
                rating = int(parts[6]) if parts[6] != "None" else None

                loans[loan_id] = Loan(
                    loan_id, member_id, book_id, loan_date, return_date, status, rating
                )

    except FileNotFoundError:
        return {}

    return loans


# ---------------------------------------------------------
# SAVE LOANS
# ---------------------------------------------------------
def save_loans_to_txt(filename, loans):
    with open(filename, "w", encoding="utf-8") as f:
        for l in loans.values():
            f.write(
                f"{l.loan_id}|{l.member_id}|{l.book_id}|{l.loan_date}|"
                f"{l.return_date}|{l.status}|{l.rating}\n"
            )
