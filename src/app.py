import tkinter as tk
from tkinter import ttk
from screens.home_screen import HomeScreen
from screens.login_toplevel import LoginWindow
from screens.admin_mode_screen import AdminScreen
from api import ServerAPI
from packages.server import Server

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.api = ServerAPI()
        self.root.title("La pinga de la ponga")
        self.root.geometry("600x400")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.user = None

        self.frames = {}
        for fr in (HomeScreen, AdminScreen):
            frame = fr(self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.showScreen(HomeScreen)
        self.displayMenu()

        #DEBUG##############
        self.api.login("a", "a")
        self.enable_admin_mode()
        for i in range(1, 20):
            try:
                self.api.create_camera(f"camera{i}", "a")
            except:
                pass
        #####################

        self.root.mainloop()

    def showScreen(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def displayMenu(self):
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu = self.main_menu)

        self.main_menu.add_command(label = "Log in", command=self.login)

    def displayAdminMenu(self):
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu = self.main_menu)

        self.user_menu = tk.Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="User", menu=self.user_menu)
        self.user_menu.add_command(label = "Log out", command=self.log_out)
        self.user_menu.add_command(label = "Change Password")

        self.main_menu.add_command(label = "Dencrypt")

    def log_out(self):
        self.api.logout()
        self.disable_admin_mode()

    def login(self):
        LoginWindow(self)

    def enable_admin_mode(self):
        self.frames[AdminScreen].initiate_main_display()
        self.showScreen(AdminScreen)
        self.displayAdminMenu()

    def disable_admin_mode(self):
        self.showScreen(HomeScreen)
        self.displayMenu()

if __name__ == '__main__':
    """s = Server()
    for i in range(9, 19):
        s.create_camera(f"camera{i}", "a")"""
    a = App()