import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from .login_toplevel import LoginWindow
from .register_toplevel import RegisterWindow
import platform

class HomeScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="#212121")
        self.pack(fill=tk.BOTH, expand=True)
        self.app = app

    def initiate_main_display(self):
        # First, if the frame is not empty, we destroy all the widgets
        for w in self.winfo_children():
            w.destroy()
        # Then, we create the main menu
        self.create_main_menu()
        # We create a canvas to put the scrollbar in it
        # Calculate de height that the menu is taking
        self.canvas = tk.Canvas(self, background="#212121", highlightthickness=0, borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # We configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.canvas_reconfigure)

        self.show_images()
        if platform.system() == "Windows" or platform.system() == "MacOS":
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        else:
            # Binding buttons are different in Linux
            self.canvas.bind_all("<Button-4>", self.on_mousewheel_up)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel_down)

    def canvas_reconfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def on_mousewheel_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_main_menu(self):
        self.main_menu = tk.Menu(self.app.root)
        self.app.root.config(menu=self.main_menu)

        # We create the file menu
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.app.root.quit)

        # We create the user menu
        self.user_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="User", menu=self.user_menu)
        self.user_menu.add_command(label="Login", command=self.login)
        self.user_menu.add_command(label="Register", command=self.register)

    def show_images(self):
        # If the user is not logged in it will raise an exception

        for i in range(20):
            new_frame = tk.Frame(self.canvas, background="#454545")
            self.canvas.create_window((0, i * 70),
                                      window=new_frame,
                                      anchor=tk.CENTER,
                                      width=300)
            tk.Label(new_frame,
                     text="La pinga de la ponga",
                     background="#454545",
                     foreground="#ffffff").pack(side=tk.LEFT, padx=10, pady=10)

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self.initiate_main_display()

    def login(self):
        LoginWindow(self.app)

    def register(self):
        RegisterWindow(self.app)