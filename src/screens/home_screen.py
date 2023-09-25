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
        self.images = self.app.api.get_images(self.rows * self.columns)
        self.update_images()
        # print(len(images))

    def update_images(self):
        for row in range(self.rows):
            for col in range(self.columns):
                index = (row + 1)*(col + 1)-1
                if index >= len(self.images):
                    lab = tk.Label(self, text="No signal", bg="#212121", fg="#ffffff")
                else:
                    camera = ImageTk.PhotoImage(self.escale_image(self.images[index]))
                    self.camera_images.append(camera)
                    lab = tk.Label(self, image=camera)
                lab.grid(row=row, column=col, sticky=tk.NSEW, padx=10, pady=10)

    def escale_image(self, image):
        width, height = image.size
        max_width = self.winfo_width()//self.columns
        max_height = self.winfo_height()//self.rows
        if max_height <= 1 or max_width <= 1:
            max_width = 600
            max_height = 400
        ratio = max(max_width/width, max_height/height)

        return image.resize((int(width*ratio), int(height*ratio)))


    def on_resize(self, event):
        for row in range(self.rows):
            self.grid_rowconfigure(row, weight=1)
        for col in range(self.columns):
            self.grid_columnconfigure(col, weight=1)