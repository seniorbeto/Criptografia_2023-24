import tkinter as tk

class LoadingScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#525252")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.loading_label = tk.Label(self, text="Loading...", background="#212121", foreground="#ffffff")
        self.loading_label.pack(padx=10, pady=15)
