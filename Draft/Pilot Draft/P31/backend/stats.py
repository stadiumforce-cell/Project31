# backend/stats.py

from datetime import date
from collections import defaultdict
from typing import Dict, List
from backend.models import Loan, Book, Member


# ---------------------------------------------------------
# ΒΟΗΘΗΤΙΚΗ ΣΥΝΑΡΤΗΣΗ: Έλεγχος αν δανεισμός είναι σε περίοδο
# ---------------------------------------------------------

def loan_in_period(loan: Loan, start: date, end: date) -> bool:
    return start <= loan.loan_date <= end


# ---------------------------------------------------------
# 1. Πλήθος βιβλίων ανά μέλος σε χρονική περίοδο
# ---------------------------------------------------------

def loans_per_member(loans: Dict[int, Loan], member_id: int, start: date, end: date) -> int:
    return sum(
        1 for loan in loans.values()
        if loan.member_id == member_id and loan_in_period(loan, start, end)
    )


# ---------------------------------------------------------
# 2. Κατανομή προτιμήσεων δανεισμού ανά μέλος (ανά κατηγορία)
# ---------------------------------------------------------

def member_category_preferences(
    loans: Dict[int, Loan],
    books: Dict[int, Book],
    member_id: int,
    start: date,
    end: date
) -> Dict[str, int]:

    categories = defaultdict(int)

    for loan in loans.values():
        if loan.member_id == member_id and loan_in_period(loan, start, end):
            book = books.get(loan.book_id)
            if book:
                categories[book.category] += 1

    return dict(categories)


# ---------------------------------------------------------
# 3. Κατανομή προτιμήσεων όλων των μελών ανά κατηγορία
# ---------------------------------------------------------

def global_category_distribution(
    loans: Dict[int, Loan],
    books: Dict[int, Book],
    start: date,
    end: date
) -> Dict[str, int]:

    categories = defaultdict(int)

    for loan in loans.values():
        if loan_in_period(loan, start, end):
            book = books.get(loan.book_id)
            if book:
                categories[book.category] += 1

    return dict(categories)


# ---------------------------------------------------------
# 4. Πλήθος δανεισμών ανά συγγραφέα
# ---------------------------------------------------------

def loans_per_author(
    loans: Dict[int, Loan],
    books: Dict[int, Book],
    start: date,
    end: date
) -> Dict[str, int]:

    authors = defaultdict(int)

    for loan in loans.values():
        if loan_in_period(loan, start, end):
            book = books.get(loan.book_id)
            if book:
                authors[book.author] += 1

    return dict(authors)


# ---------------------------------------------------------
# 5. Πλήθος δανεισμών ανά ηλικία
# ---------------------------------------------------------

def loans_per_age(
    loans: Dict[int, Loan],
    members: Dict[int, Member],
    start: date,
    end: date
) -> Dict[int, int]:

    ages = defaultdict(int)

    for loan in loans.values():
        if loan_in_period(loan, start, end):
            member = members.get(loan.member_id)
            if member:
                ages[member.age] += 1

    return dict(ages)


# ---------------------------------------------------------
# 6. Πλήθος δανεισμών ανά φύλο
# ---------------------------------------------------------

def loans_per_gender(
    loans: Dict[int, Loan],
    members: Dict[int, Member],
    start: date,
    end: date
) -> Dict[str, int]:

    genders = defaultdict(int)

    for loan in loans.values():
        if loan_in_period(loan, start, end):
            member = members.get(loan.member_id)
            if member:
                genders[member.gender] += 1

    return dict(genders)


# ---------------------------------------------------------
# 7. Ιστορικό δανεισμών ανά μέλος
# ---------------------------------------------------------

def member_loan_history(
    loans: Dict[int, Loan],
    books: Dict[int, Book],
    member_id: int
) -> List[dict]:

    history = []

    for loan in loans.values():
        if loan.member_id == member_id:
            book = books.get(loan.book_id)
            history.append({
                "loan_id": loan.loan_id,
                "book_title": book.title if book else "Unknown",
                "loan_date": loan.loan_date,
                "return_date": loan.return_date,
                "status": loan.status,
                "rating": loan.rating
            })

    return history
