import tkinter as tk
from tkinter import ttk

class HomeScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#212121")
        self.pack(fill=tk.BOTH, expand=True)
        parent.bind("<Configure>", self.on_resize)

        self.rows = 4
        self.columns = 4

        for row in range(self.rows):
            for col in range(self.columns):
                # Aquí hay que sustituir el label por un canvas con la imagen de la cámara
                camera = tk.Label(self, text=f"Camera {row*col}")
                camera.grid(row=row, column=col, sticky=tk.NSEW)


    def on_resize(self, event):
        for row in range(self.rows):
            self.grid_rowconfigure(row, weight=1)
        for col in range(self.columns):
            self.grid_columnconfigure(col, weight=1)
