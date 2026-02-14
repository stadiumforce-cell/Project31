# gui/members_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from gui.forms import FormPopup


class MembersView(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)

        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Διαχείριση Μελών", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Προσθήκη Μέλους", width=25, command=self.add_member).pack(pady=5)
        tk.Button(self, text="Ανανέωση Λίστας", width=25, command=self.refresh).pack(pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Όνομα")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.refresh()

    # -----------------------------
    # Add Member
    # -----------------------------
    def add_member(self):
        fields = {
            "Όνομα": "",
            "Διεύθυνση": "",
            "Τηλέφωνο": "",
            "Email": "",
            "Ηλικία": "",
            "Επάγγελμα": "",
            "Φύλο": ""
        }

        def submit(data):
            try:
                self.manager.add_member(
                    data["Όνομα"],
                    data["Διεύθυνση"],
                    data["Τηλέφωνο"],
                    data["Email"],
                    int(data["Ηλικία"]),
                    data["Επάγγελμα"],
                    data["Φύλο"]
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Νέο Μέλος", fields, submit)

    # -----------------------------
    # Refresh Tree
    # -----------------------------
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for m in self.manager.get_all_members():
            self.tree.insert("", "end", values=(m.member_id, m.name, m.email))
