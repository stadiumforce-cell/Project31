# gui/forms.py

import tkinter as tk
from tkinter import ttk


class FormPopup(tk.Toplevel):
    def __init__(self, title, fields, on_submit):
        super().__init__()
        self.title(title)
        self.values = {}
        self.on_submit = on_submit

        for i, (label, default) in enumerate(fields.items()):
            tk.Label(self, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, default)
            self.values[label] = entry

        tk.Button(self, text="OK", command=self.submit).grid(
            row=len(fields), column=0, columnspan=2, pady=10
        )

    def submit(self):
        data = {label: entry.get() for label, entry in self.values.items()}
        self.on_submit(data)
        self.destroy()
