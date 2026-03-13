import tkinter as tk
from database import init_db
from gui import SortifyGUI

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = SortifyGUI(root)
    root.mainloop()