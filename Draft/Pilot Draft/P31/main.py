# main.py

from gui.app import LibraryApp
from backend.manager import LibraryManager

def main():
    manager = LibraryManager()   # φορτώνει τα δεδομένα στη μνήμη
    app = LibraryApp(manager)    # δημιουργεί το GUI
    app.mainloop()               # ξεκινάει το παράθυρο

if __name__ == "__main__":
    main()
