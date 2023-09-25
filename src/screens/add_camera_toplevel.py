import tkinter as tk
from tkinter import messagebox

class AddCameraWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.geometry("200x300")
        self.resizable(False, False)
        self.title("Add Camera")
        self.app = app

        # Username
        self.username_label = tk.Label(self, text="Camera Name", background="#212121", foreground="#ffffff")
        self.username_label.pack(padx=10, pady=15)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=10, pady=15)

        #############################
        button = tk.Button(self, text="APAÑAO", command=self.add_cam)
        button.pack(padx=10, pady=30)

    def add_cam(self):
        cam_name = self.username_entry.get()
        self.app.api.create_camera(cam_name, self.app.api.username)
        self.destroy()