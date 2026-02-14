# gui/stats_view.py

import tkinter as tk
from tkinter import ttk


class StatsView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Στατιστικά", font=("Arial", 18)).pack(pady=20)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Ανά Μέλος", width=20, command=self.show_member_stats).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Ανά Κατηγορία", width=20, command=self.show_category_stats).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Ανά Συγγραφέα", width=20, command=self.show_author_stats).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Ανά Ηλικία", width=20, command=self.show_age_stats).grid(row=0, column=3, padx=5)

        # Output area
        self.output = tk.Text(self, height=20)
        self.output.pack(fill="both", expand=True, pady=20)

    # ---------------------------------------------------------
    # Helper: εμφανίζει λεξικό στατιστικών
    # ---------------------------------------------------------
    def display_stats(self, title, stats_dict):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"{title}\n")
        self.output.insert(tk.END, "-" * 40 + "\n")

        if not stats_dict:
            self.output.insert(tk.END, "Δεν υπάρχουν δεδομένα.\n")
            return

        for key, value in stats_dict.items():
            self.output.insert(tk.END, f"{key}: {value}\n")

    # ---------------------------------------------------------
    # Στατιστικά ανά μέλος
    # ---------------------------------------------------------
    def show_member_stats(self):
        stats = self.manager.stats_loans_per_member()
        readable = {f"Μέλος {mid}": count for mid, count in stats.items()}
        self.display_stats("Στατιστικά Δανεισμών ανά Μέλος", readable)

    # ---------------------------------------------------------
    # Στατιστικά ανά κατηγορία
    # ---------------------------------------------------------
    def show_category_stats(self):
        stats = self.manager.stats_loans_per_category()
        self.display_stats("Στατιστικά Δανεισμών ανά Κατηγορία", stats)

    # ---------------------------------------------------------
    # Στατιστικά ανά συγγραφέα
    # ---------------------------------------------------------
    def show_author_stats(self):
        stats = self.manager.stats_loans_per_author()
        self.display_stats("Στατιστικά Δανεισμών ανά Συγγραφέα", stats)

    # ---------------------------------------------------------
    # Στατιστικά ανά ηλικιακή ομάδα
    # ---------------------------------------------------------
    def show_age_stats(self):
        stats = self.manager.stats_loans_per_age_group()
        self.display_stats("Στατιστικά Δανεισμών ανά Ηλικιακή Ομάδα", stats)
