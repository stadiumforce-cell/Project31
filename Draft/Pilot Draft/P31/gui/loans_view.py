# gui/loans_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from gui.forms import FormPopup


class LoansView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Διαχείριση Δανεισμών", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Νέος Δανεισμός", width=25, command=self.new_loan).pack(pady=5)
        tk.Button(self, text="Επιστροφή Βιβλίου", width=25, command=self.return_loan).pack(pady=5)
        tk.Button(self, text="Ανανέωση Λίστας", width=25, command=self.refresh).pack(pady=5)

        self.tree = ttk.Treeview(self, columns=("LoanID", "Member", "Book", "Status"), show="headings")
        self.tree.heading("LoanID", text="ID")
        self.tree.heading("Member", text="Μέλος")
        self.tree.heading("Book", text="Βιβλίο")
        self.tree.heading("Status", text="Κατάσταση")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.refresh()

    def new_loan(self):
        fields = {
            "ID Μέλους": "",
            "ID Βιβλίου": ""
        }

        def submit(data):
            try:
                self.manager.create_loan(
                    int(data["ID Μέλους"]),
                    int(data["ID Βιβλίου"])
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Νέος Δανεισμός", fields, submit)

    def return_loan(self):
        fields = {
            "ID Δανεισμού": "",
            "Rating (1-5 ή κενό)": ""
        }

        def submit(data):
            try:
                rating = data["Rating (1-5 ή κενό)"]
                rating = int(rating) if rating else None

                self.manager.return_loan(
                    int(data["ID Δανεισμού"]),
                    rating=rating
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Επιστροφή Βιβλίου", fields, submit)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row
