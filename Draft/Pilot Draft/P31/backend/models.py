# backend/models.py

from dataclasses import dataclass
from datetime import date
from typing import Optional


# ---------------------------------------------------------
# ΜΕΛΟΣ
# ---------------------------------------------------------

@dataclass
class Member:
    member_id: int
    name: str
    address: str
    phone: str
    email: str
    age: int
    profession: str
    gender: str
    active: bool = True

    def __repr__(self):
        return f"<Member {self.member_id}: {self.name}, active={self.active}>"


# ---------------------------------------------------------
# ΒΙΒΛΙΟ
# ---------------------------------------------------------

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    category: str
    isbn: str
    stock: int
    total_loans: int = 0

    def __repr__(self):
        return f"<Book {self.book_id}: {self.title} ({self.stock} διαθέσιμα)>"


# ---------------------------------------------------------
# ΔΑΝΕΙΣΜΟΣ
# ---------------------------------------------------------

@dataclass
class Loan:
    loan_id: int
    member_id: int
    book_id: int
    loan_date: date
    return_date: Optional[date]
    status: str  # "active" ή "returned"
    rating: Optional[int] = None  # 1–5 ή None

    def __repr__(self):
        return f"<Loan {self.loan_id}: member={self.member_id}, book={self.book_id}, status={self.status}>"


# ---------------------------------------------------------
# ΠΡΟΑΙΡΕΤΙΚΗ ΚΑΤΗΓΟΡΙΑ
# ---------------------------------------------------------

@dataclass
class Category:
    name: str
    description: Optional[str] = None

    def __repr__(self):
        return f"<Category {self.name}>"
