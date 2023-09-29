import tkinter as tk
from PIL import Image, ImageTk
import platform

class UserScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.app = app
        self.cache_images = []

    def initiate_main_display(self):
        # First, if the frame is not empty, we destroy all the widgets
        for w in self.winfo_children():
            w.destroy()

        self.display_main_menu()

        self.app.root.title(f"Logged as: {self.app.api.username}")

        # We create a canvas to put the scrollbar in it
        # Calculate de height that the menu is taking
        self.canvas = tk.Canvas(self, background="#212121", highlightthickness=0, borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
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


    def display_main_menu(self):
        self.main_menu = tk.Menu(self.app.root)
        self.app.root.config(menu=self.main_menu)

        # We create the file menu
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Image", command=self.add_image)
        self.file_menu.add_command(label="Exit", command=self.app.root.quit)

        # We create the user menu
        self.user_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="User", menu=self.user_menu)
        self.user_menu.add_command(label="Logout", command=self.logout)
        self.user_menu.add_command(label="Change Password")

    def logout(self):
        self.app.api.logout()
        self.app.showHomeScreen()

    def show_images(self):
        self.images = self.app.api.get_images(date="2022") # Date is temporal until issue #15 is solved
        y = 0
        for i in range(len(self.images)):
            image = ImageTk.PhotoImage(self.images[i].resize((200, 200)))
            self.cache_images.append(image)
            image_label = tk.Label(self.canvas, image=image)
            if i%3 == 0:
                y += 200
            self.canvas.create_window(((i%3)*200, y), window=image_label, anchor="nw")

    def add_image(self):...
