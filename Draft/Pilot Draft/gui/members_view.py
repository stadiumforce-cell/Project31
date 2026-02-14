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

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Προσθήκη Μέλους", width=20, command=self.add_member).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Επεξεργασία Μέλους", width=20, command=self.edit_member).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Διαγραφή Μέλους", width=20, command=self.delete_member).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Ανανέωση", width=20, command=self.refresh).grid(row=0, column=3, padx=5)

        # TreeView
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Όνομα")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.refresh()

    # ---------------------------------------------------------
    # Προσθήκη μέλους
    # ---------------------------------------------------------
    def add_member(self):
        fields = {
            "Όνομα": "",
            "Διεύθυνση": "",
            "Τηλέφωνο": "",
            "Email": "",
            "Ηλικία": "",
            "Επάγγελμα": ""
        }

        def submit(data):
            try:
                self.manager.add_member(
                    data["Όνομα"],
                    data["Διεύθυνση"],
                    data["Τηλέφωνο"],
                    data["Email"],
                    int(data["Ηλικία"]),
                    data["Επάγγελμα"]
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Νέο Μέλος", fields, submit)

    # ---------------------------------------------------------
    # Επεξεργασία μέλους
    # ---------------------------------------------------------
    def edit_member(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα μέλος.")
            return

        member_id = int(self.tree.item(selected[0])["values"][0])
        member = self.manager.members[member_id]

        fields = {
            "Όνομα": member.name,
            "Διεύθυνση": member.address,
            "Τηλέφωνο": member.phone,
            "Email": member.email,
            "Ηλικία": str(member.age),
            "Επάγγελμα": member.profession
        }

        def submit(data):
            try:
                self.manager.update_member(
                    member_id,
                    name=data["Όνομα"],
                    address=data["Διεύθυνση"],
                    phone=data["Τηλέφωνο"],
                    email=data["Email"],
                    age=int(data["Ηλικία"]),
                    profession=data["Επάγγελμα"]
                )
                self.manager.save_all()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Σφάλμα", str(e))

        FormPopup("Επεξεργασία Μέλους", fields, submit)

    # ---------------------------------------------------------
    # Διαγραφή μέλους
    # ---------------------------------------------------------
    def delete_member(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα μέλος.")
            return

        member_id = int(self.tree.item(selected[0])["values"][0])

        if not messagebox.askyesno("Επιβεβαίωση", "Θέλετε σίγουρα να διαγράψετε το μέλος;"):
            return

        try:
            self.manager.delete_member(member_id)
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

        for m in self.manager.get_all_members():
            self.tree.insert("", "end", values=(m.member_id, m.name, m.email))
