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

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Προσθήκη Βιβλίου", width=20, command=self.add_book).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Επεξεργασία Βιβλίου", width=20, command=self.edit_book).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Διαγραφή Βιβλίου", width=20, command=self.delete_book).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Ανανέωση", width=20, command=self.refresh).grid(row=0, column=3, padx=5)

        # TreeView
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Τίτλος")
        self.tree.heading("Author", text="Συγγραφέας")
        self.tree.heading("Stock", text="Απόθεμα")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.refresh()

    # ---------------------------------------------------------
    # Προσθήκη βιβλίου
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Επεξεργασία βιβλίου
    # ---------------------------------------------------------
    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα βιβλίο.")
            return

        book_id = int(self.tree.item(selected[0])["values"][0])
        book = self.manager.books[book_id]

        fields = {
            "Τίτλος": book.title,
            "Συγγραφέας": book.author,
            "Κατηγορία": book.category,
            "ISBN": book.isbn,
            "Απόθεμα": str(book.stock)
        }

        def submit(data):
            try:
                self.manager.update_book(
                    book_id,
                    title=data["Τίτλος"],
                    author=data["Συγγραφέας"],
                    category=data["Κατηγορία"],
                    isbn=data["ISBN"],
                    stock=int(data["Απόθεμα"])
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Επεξεργασία Βιβλίου", fields, submit)

    # ---------------------------------------------------------
    # Διαγραφή βιβλίου
    # ---------------------------------------------------------
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα βιβλίο.")
            return

        book_id = int(self.tree.item(selected[0])["values"][0])

        if not messagebox.askyesno("Επιβεβαίωση", "Θέλετε σίγουρα να διαγράψετε το βιβλίο;"):
            return

        try:
            self.manager.delete_book(book_id)
            self.manager.save_all()
            self.refresh()
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))

    # ---------------------------------------------------------
    # Ανανέωση λίστας
    # ---------------------------------------------------------
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for b in self.manager.get_all_books():
            self.tree.insert("", "end", values=(b.book_id, b.title, b.author, b.stock))
