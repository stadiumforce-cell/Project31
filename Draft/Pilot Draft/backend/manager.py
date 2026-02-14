# backend/manager.py

import os
from datetime import date
from backend.models import Member, Book, Loan
from backend.storage_txt import (
    load_members_from_txt, load_books_from_txt, load_loans_from_txt,
    save_members_to_txt, save_books_to_txt, save_loans_to_txt
)
from backend.recommendations import recommend_books_for_member


class LibraryManager:
    def __init__(self):

        # Ensure data folder exists
        if not os.path.exists("data"):
            os.makedirs("data")

        # Ensure required files exist
        required_files = [
            "data/members.txt",
            "data/books.txt",
            "data/loans.txt"
        ]

        for file in required_files:
            if not os.path.exists(file):
                with open(file, "w", encoding="utf-8") as f:
                    pass

        # Load data
        self.members = load_members_from_txt("data/members.txt")
        self.books = load_books_from_txt("data/books.txt")
        self.loans = load_loans_from_txt("data/loans.txt")

        # Auto-increment IDs
        self.next_member_id = max(self.members.keys(), default=0) + 1
        self.next_book_id = max(self.books.keys(), default=0) + 1
        self.next_loan_id = max(self.loans.keys(), default=0) + 1

    # ---------------------------------------------------------
    # SAVE ALL
    # ---------------------------------------------------------
    def save_all(self):
        save_members_to_txt("data/members.txt", self.members)
        save_books_to_txt("data/books.txt", self.books)
        save_loans_to_txt("data/loans.txt", self.loans)

    # ---------------------------------------------------------
    # ΜΕΛΗ
    # ---------------------------------------------------------

    def add_member(self, name, address, phone, email, age, profession):
        member = Member(
            member_id=self.next_member_id,
            name=name,
            address=address,
            phone=phone,
            email=email,
            age=age,
            profession=profession,
            active=True
        )
        self.members[self.next_member_id] = member
        self.next_member_id += 1
        return member

    def update_member(self, member_id, **fields):
        if member_id not in self.members:
            raise ValueError("Το μέλος δεν υπάρχει.")

        member = self.members[member_id]

        for key, value in fields.items():
            if hasattr(member, key):
                setattr(member, key, value)

        return member

    def delete_member(self, member_id):
        if member_id not in self.members:
            raise ValueError("Το μέλος δεν υπάρχει.")

        active_loans = [
            l for l in self.loans.values()
            if l.member_id == member_id and l.status == "active"
        ]
        if active_loans:
            raise ValueError("Το μέλος έχει ενεργούς δανεισμούς.")

        del self.members[member_id]

    def search_members(self, keyword):
        keyword = keyword.lower()
        return [
            m for m in self.members.values()
            if keyword in m.name.lower() or keyword in m.email.lower()
        ]

    def get_all_members(self):
        return list(self.members.values())

    # ---------------------------------------------------------
    # ΒΙΒΛΙΑ
    # ---------------------------------------------------------

    def add_book(self, title, author, category, isbn, stock):
        book = Book(
            book_id=self.next_book_id,
            title=title,
            author=author,
            category=category,
            isbn=isbn,
            stock=stock,
            total_loans=0
        )
        self.books[self.next_book_id] = book
        self.next_book_id += 1
        return book

    def update_book(self, book_id, **fields):
        if book_id not in self.books:
            raise ValueError("Το βιβλίο δεν υπάρχει.")

        book = self.books[book_id]

        for key, value in fields.items():
            if hasattr(book, key):
                setattr(book, key, value)

        return book

    def delete_book(self, book_id):
        if book_id not in self.books:
            raise ValueError("Το βιβλίο δεν υπάρχει.")

        active_loans = [
            l for l in self.loans.values()
            if l.book_id == book_id and l.status == "active"
        ]
        if active_loans:
            raise ValueError("Το βιβλίο είναι δανεισμένο.")

        del self.books[book_id]

    def search_books(self, keyword=None, category=None, author=None, title=None):
        results = list(self.books.values())

        if keyword:
            keyword = keyword.lower()
            results = [
                b for b in results
                if keyword in b.title.lower() or keyword in b.author.lower()
            ]

        if category:
            results = [b for b in results if b.category == category]

        if author:
            results = [b for b in results if author.lower() in b.author.lower()]

        if title:
            results = [b for b in results if title.lower() in b.title.lower()]

        return results

    def get_available_books(self, category=None):
        books = self.books.values()
        if category:
            books = [b for b in books if b.category == category]
        return [b for b in books if b.stock > 0]

    def check_availability(self, book_id):
        if book_id not in self.books:
            raise ValueError("Το βιβλίο δεν υπάρχει.")
        return self.books[book_id].stock > 0

    def get_all_books(self):
        return list(self.books.values())

    # ---------------------------------------------------------
    # ΔΑΝΕΙΣΜΟΙ
    # ---------------------------------------------------------

    def create_loan(self, member_id, book_id, loan_date=None):
        if member_id not in self.members:
            raise ValueError("Το μέλος δεν υπάρχει.")

        if book_id not in self.books:
            raise ValueError("Το βιβλίο δεν υπάρχει.")

        if not self.check_availability(book_id):
            raise ValueError("Το βιβλίο δεν είναι διαθέσιμο.")

        if loan_date is None:
            loan_date = date.today()

        loan = Loan(
            loan_id=self.next_loan_id,
            member_id=member_id,
            book_id=book_id,
            loan_date=loan_date,
            return_date=None,
            status="active",
            rating=None
        )

        self.loans[self.next_loan_id] = loan
        self.next_loan_id += 1

        self.books[book_id].stock -= 1
        self.books[book_id].total_loans += 1

        return loan

    def return_loan(self, loan_id, return_date=None, rating=None):
        if loan_id not in self.loans:
            raise ValueError("Ο δανεισμός δεν υπάρχει.")

        loan = self.loans[loan_id]

        if loan.status == "returned":
            raise ValueError("Το βιβλίο έχει ήδη επιστραφεί.")

        if return_date is None:
            return_date = date.today()

        loan.return_date = return_date
        loan.status = "returned"
        loan.rating = rating

        self.books[loan.book_id].stock += 1

        return loan

    def get_member_loans(self, member_id, active_only=False):
        if member_id not in self.members:
            raise ValueError("Το μέλος δεν υπάρχει.")

        loans = [
            l for l in self.loans.values()
            if l.member_id == member_id
        ]

        if active_only:
            loans = [l for l in loans if l.status == "active"]

        return loans

    def get_all_loans(self):
        return list(self.loans.values())

    # ---------------------------------------------------------
    # ΣΤΑΤΙΣΤΙΚΑ (χωρίς φύλο)
    # ---------------------------------------------------------

    def stats_loans_per_member(self):
        stats = {}
        for loan in self.loans.values():
            stats[loan.member_id] = stats.get(loan.member_id, 0) + 1
        return stats

    def stats_loans_per_category(self):
        stats = {}
        for loan in self.loans.values():
            book = self.books.get(loan.book_id)
            if book:
                stats[book.category] = stats.get(book.category, 0) + 1
        return stats

    def stats_loans_per_author(self):
        stats = {}
        for loan in self.loans.values():
            book = self.books.get(loan.book_id)
            if book:
                stats[book.author] = stats.get(book.author, 0) + 1
        return stats

    def stats_loans_per_age_group(self):
        stats = {"0-17": 0, "18-30": 0, "31-50": 0, "51+": 0}
        for loan in self.loans.values():
            member = self.members.get(loan.member_id)
            if member:
                age = member.age
                if age <= 17:
                    stats["0-17"] += 1
                elif age <= 30:
                    stats["18-30"] += 1
                elif age <= 50:
                    stats["31-50"] += 1
                else:
                    stats["51+"] += 1
        return stats

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    def get_recommendations(self, member_id, top_n=5):
        return recommend_books_for_member(
            member_id,
            self.members,
            self.books,
            self.loans,
            top_n
        )
