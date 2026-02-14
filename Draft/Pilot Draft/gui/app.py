# gui/app.py

import tkinter as tk
from tkinter import ttk

from gui.members_view import MembersView
from gui.books_view import BooksView
from gui.loans_view import LoansView
from gui.stats_view import StatsView
from gui.recommend_view import RecommendView


class LibraryApp(tk.Tk):
    def __init__(self, manager):
        super().__init__()

        self.title("Σύστημα Διαχείρισης Δανειστικής Βιβλιοθήκης")
        self.geometry("900x600")

        self.manager = manager

        # Container για όλα τα frames
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Καταχώρηση όλων των views
        for F in (MembersView, BooksView, LoansView, StatsView, RecommendView):
            frame = F(container, self, manager)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Navigation menu
        self.create_menu()

        # Default view
        self.show_frame(MembersView)

    def create_menu(self):
        menubar = tk.Menu(self)

        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Μέλη", command=lambda: self.show_frame(MembersView))
        menu.add_command(label="Βιβλία", command=lambda: self.show_frame(BooksView))
        menu.add_command(label="Δανεισμοί", command=lambda: self.show_frame(LoansView))
        menu.add_command(label="Στατιστικά", command=lambda: self.show_frame(StatsView))
        menu.add_command(label="Προτάσεις", command=lambda: self.show_frame(RecommendView))

        menubar.add_cascade(label="Μενού", menu=menu)
        self.config(menu=menubar)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
