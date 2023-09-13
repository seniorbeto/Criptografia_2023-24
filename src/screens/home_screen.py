import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class HomeScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="#212121")
        self.pack(fill=tk.BOTH, expand=True)
        app.root.bind("<Configure>", self.on_resize)

        self.app = app
        self.rows = 4
        self.columns = 4
        self.camera_images = []
        images = self.app.api_server.getCameraImages(self.rows * self.columns)
        print(len(images))

        for row in range(self.rows):
            for col in range(self.columns):
                index = (row + 1)*(col + 1)-1
                if index >= len(images):
                    lab = tk.Label(self, text="No signal", bg="#212121", fg="#ffffff")
                else:
                    camera = ImageTk.PhotoImage(images[index])
                    self.camera_images.append(camera)
                    lab = tk.Label(self, image=camera)
                lab.grid(row=row, column=col, sticky=tk.NSEW, padx=10, pady=10)


    def on_resize(self, event):
        for row in range(self.rows):
            self.grid_rowconfigure(row, weight=1)
        for col in range(self.columns):
            self.grid_columnconfigure(col, weight=1)
