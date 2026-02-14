# gui/recommend_view.py

import tkinter as tk
from tkinter import ttk


class RecommendView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Προτάσεις Βιβλίων", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="ID Μέλους:").pack()
        self.member_entry = tk.Entry(self)
        self.member_entry.pack()

        tk.Button(self, text="Προβολή Προτάσεων", command=self.show_recommendations).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Category"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Τίτλος")
        self.tree.heading("Category", text="Κατηγορία")
        self.tree.pack(fill="both", expand=True, pady=20)

    def show_recommendations(self):
        member_id = int(self.member_entry.get())
        books = self.manager.get_recommendations(member_id)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in books:
            self.tree.insert("", "end", values=(book.book_id, book.title, book.category))
