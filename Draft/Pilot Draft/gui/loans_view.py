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

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Νέος Δανεισμός", width=20, command=self.new_loan).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Επιστροφή Βιβλίου", width=20, command=self.return_loan).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Διαγραφή Δανεισμού", width=20, command=self.delete_loan).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Ανανέωση", width=20, command=self.refresh).grid(row=0, column=3, padx=5)

        # TreeView
        self.tree = ttk.Treeview(self, columns=("LoanID", "Member", "Book", "Status"), show="headings")
        self.tree.heading("LoanID", text="ID")
        self.tree.heading("Member", text="Μέλος")
        self.tree.heading("Book", text="Βιβλίο")
        self.tree.heading("Status", text="Κατάσταση")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.refresh()

    # ---------------------------------------------------------
    # Νέος Δανεισμός
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Επιστροφή Βιβλίου
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Διαγραφή Δανεισμού
    # ---------------------------------------------------------
    def delete_loan(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε έναν δανεισμό.")
            return

        loan_id = int(self.tree.item(selected[0])["values"][0])
        loan = self.manager.loans[loan_id]

        if loan.status == "active":
            messagebox.showerror("Σφάλμα", "Δεν μπορείτε να διαγράψετε ενεργό δανεισμό.")
            return

        if not messagebox.askyesno("Επιβεβαίωση", "Θέλετε σίγουρα να διαγράψετε τον δανεισμό;"):
            return

        try:
            del self.manager.loans[loan_id]
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

        for l in self.manager.get_all_loans():
            self.tree.insert("", "end", values=(
                l.loan_id,
                f"{l.member_id}",
                f"{l.book_id}",
                l.status
            ))
