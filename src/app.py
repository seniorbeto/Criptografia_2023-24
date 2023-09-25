import tkinter as tk
from tkinter import ttk
from screens.home_screen import HomeScreen
from screens.login_toplevel import LoginWindow
from screens.add_camera_toplevel import AddCameraWindow
from screens.admin_mode_screen import AdminScreen
from api import ServerAPI

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

        self.camera_menu = tk.Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="Camera", menu=self.camera_menu)
        self.camera_menu.add_command(label = "Add Camera", command=self.add_camera)
        self.delete_camera_menu = tk.Menu(self.camera_menu, tearoff=False)
        self.camera_menu.add_cascade(label = "Remove Camera", menu=self.delete_camera_menu)

        self.main_menu.add_command(label = "Dencrypt")

    def log_out(self):
        self.api.logout()
        self.disable_admin_mode()

    def add_camera(self):
        AddCameraWindow(self)

    def remove_camera(self):
        for cam in self.api.get_cameras():
            self.delete_camera_menu.add_command(label=cam)

    def login(self):
        LoginWindow(self)

    def enable_admin_mode(self):
        self.showScreen(AdminScreen)
        self.displayAdminMenu()

    def disable_admin_mode(self):
        self.showScreen(HomeScreen)
        self.displayMenu()

if __name__ == '__main__':
    App()