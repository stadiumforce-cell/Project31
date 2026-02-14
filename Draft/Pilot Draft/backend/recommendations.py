# backend/recommendations.py

from collections import defaultdict
from typing import Dict, List
from backend.models import Member, Book, Loan
from datetime import date


# ---------------------------------------------------------
# Βοηθητικό: Υπολογισμός προτιμήσεων κατηγοριών για μέλος
# ---------------------------------------------------------

def compute_member_preferences(loans: Dict[int, Loan], books: Dict[int, Book], member_id: int):
    category_count = defaultdict(int)

    for loan in loans.values():
        if loan.member_id == member_id:
            book = books.get(loan.book_id)
            if book:
                category_count[book.category] += 1

    return dict(category_count)


# ---------------------------------------------------------
# Βοηθητικό: Βαθμολογία βιβλίου για συγκεκριμένο μέλος
# ---------------------------------------------------------

def score_book_for_member(book: Book, member_preferences: dict):
    base_score = 0

    # 1. Προτίμηση κατηγορίας
    if book.category in member_preferences:
        base_score += member_preferences[book.category] * 10

    # 2. Δημοτικότητα βιβλίου
    base_score += book.total_loans

    return base_score


# ---------------------------------------------------------
# Κύρια συνάρτηση: Προτάσεις βιβλίων
# ---------------------------------------------------------

def recommend_books_for_member(
    member_id: int,
    members: Dict[int, Member],
    books: Dict[int, Book],
    loans: Dict[int, Loan],
    top_n: int = 5
) -> List[Book]:

    if member_id not in members:
        raise ValueError("Το μέλος δεν υπάρχει.")

    # 1. Προτιμήσεις μέλους
    preferences = compute_member_preferences(loans, books, member_id)

    # 2. Βιβλία που έχει ήδη δανειστεί
    borrowed_book_ids = {
        loan.book_id for loan in loans.values() if loan.member_id == member_id
    }

    # 3. Υπολογισμός score για κάθε βιβλίο
    scored_books = []

    for book in books.values():
        if book.book_id in borrowed_book_ids:
            continue  # μην προτείνεις βιβλία που έχει ήδη διαβάσει

        if book.stock <= 0:
            continue  # μην προτείνεις μη διαθέσιμα βιβλία

        score = score_book_for_member(book, preferences)
        scored_books.append((score, book))

    # 4. Ταξινόμηση κατά score
    scored_books.sort(key=lambda x: x[0], reverse=True)

    # 5. Επιστροφή top_n βιβλίων
    return [book for score, book in scored_books[:top_n]]
