# gui/stats_view.py

import tkinter as tk
from tkinter import ttk


class StatsView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Στατιστικά", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Στατιστικά ανά Μέλος", width=25).pack(pady=5)
        tk.Button(self, text="Στατιστικά ανά Κατηγορία", width=25).pack(pady=5)
        tk.Button(self, text="Στατιστικά ανά Συγγραφέα", width=25).pack(pady=5)
        tk.Button(self, text="Στατιστικά ανά Ηλικία", width=25).pack(pady=5)
        tk.Button(self, text="Στατιστικά ανά Φύλο", width=25).pack(pady=5)

        self.output = tk.Text(self, height=15)
        self.output.pack(fill="both", expand=True, pady=20)
