import tkinter as tk

class AdminScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = tk.Label(self, text="Admin Screen (has ganao)")
        label.pack(padx=10, pady=10)