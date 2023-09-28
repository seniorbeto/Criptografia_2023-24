import tkinter as tk

class UserScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.app = app

    def initiate_main_display(self):
        # First, if the frame is not empty, we destroy all the widgets
        for w in self.winfo_children():
            w.destroy()

        self.display_main_menu()

        user_label = tk.Label(self, text="Logged as " + self.app.api.username)
        user_label.pack()


    def display_main_menu(self):
        self.main_menu = tk.Menu(self.app.root)
        self.app.root.config(menu=self.main_menu)

        # We create the file menu
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.app.root.quit)

        # We create the user menu
        self.user_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="User", menu=self.user_menu)
        self.user_menu.add_command(label="Logout", command=self.logout)
        self.user_menu.add_command(label="Change Password")

    def logout(self):
        self.app.api.logout()
        self.app.showHomeScreen()
