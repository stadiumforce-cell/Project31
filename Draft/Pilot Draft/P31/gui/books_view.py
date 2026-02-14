# gui/books_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from gui.forms import FormPopup


class BooksView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Διαχείριση Βιβλίων", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Προσθήκη Βιβλίου", width=25, command=self.add_book).pack(pady=5)
        tk.Button(self, text="Ανανέωση Λίστας", width=25, command=self.refresh).pack(pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Τίτλος")
        self.tree.heading("Author", text="Συγγραφέας")
        self.tree.heading("Stock", text="Απόθεμα")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.refresh()

    def add_book(self):
        fields = {
            "Τίτλος": "",
            "Συγγραφέας": "",
            "Κατηγορία": "",
            "ISBN": "",
            "Απόθεμα": "1"
        }

        def submit(data):
            try:
                self.manager.add_book(
                    data["Τίτλος"],
                    data["Συγγραφέας"],
                    data["Κατηγορία"],
                    data["ISBN"],
                    int(data["Απόθεμα"])
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Νέο Βιβλίο", fields, submit)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for b in self.manager.get_all_books():
            self.tree.insert("", "end", values=(b.book_id, b.title, b.author, b.stock))
