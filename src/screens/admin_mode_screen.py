import tkinter as tk

class AdminScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.app = app

        label = tk.Label(self, text="Admin Screen (has ganao)", background="#212121", foreground="#ffffff")
        label.pack(padx=10, pady=10)