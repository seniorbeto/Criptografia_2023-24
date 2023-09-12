import tkinter as tk

class AdminScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="#212121")

        label = tk.Label(self, text="Admin Screen (has ganao)", background="#212121", foreground="#ffffff")
        label.pack(padx=10, pady=10)