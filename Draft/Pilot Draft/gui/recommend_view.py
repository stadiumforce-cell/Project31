# gui/recommend_view.py

import tkinter as tk
from tkinter import ttk, messagebox


class RecommendView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Προτάσεις Βιβλίων", font=("Arial", 18)).pack(pady=20)

        # Input area
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="ID Μέλους:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.member_entry = tk.Entry(input_frame, width=10)
        self.member_entry.grid(row=0, column=1, padx=5)

        tk.Button(input_frame, text="Προβολή Προτάσεων", width=20, command=self.show_recommendations)\
            .grid(row=0, column=2, padx=10)

        # Output area
        self.output = tk.Text(self, height=20)
        self.output.pack(fill="both", expand=True, pady=20)

    # ---------------------------------------------------------
    # Εμφάνιση προτάσεων
    # ---------------------------------------------------------
    def show_recommendations(self):
        self.output.delete("1.0", tk.END)

        member_id_text = self.member_entry.get().strip()
        if not member_id_text.isdigit():
            messagebox.showerror("Σφάλμα", "Το ID μέλους πρέπει να είναι αριθμός.")
            return

        member_id = int(member_id_text)

        if member_id not in self.manager.members:
            messagebox.showerror("Σφάλμα", "Το μέλος δεν υπάρχει.")
            return

        # Λήψη προτάσεων από το backend
        recommendations = self.manager.get_recommendations(member_id)

        self.output.insert(tk.END, f"Προτάσεις για το μέλος {member_id}\n")
        self.output.insert(tk.END, "-" * 40 + "\n")

        if not recommendations:
            self.output.insert(tk.END, "Δεν υπάρχουν διαθέσιμες προτάσεις.\n")
            return

        for book in recommendations:
            self.output.insert(
                tk.END,
                f"• {book.title} — {book.author} "
                f"(Κατηγορία: {book.category}, Διαθέσιμα: {book.stock})\n"
            )
