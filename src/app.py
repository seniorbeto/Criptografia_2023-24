import tkinter as tk
from tkinter import ttk
from screens.home_screen import HomeScreen
from screens.user_screen import UserScreen
from packages.api import ServerAPI
from packages.server import Server
from packages.server.ImgPackage import ImgPackage

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.api = ServerAPI()
        self.root.title("La pinga de la ponga")
        self.root.geometry("700x400")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.user = None

        self.frames = {}
        for fr in (HomeScreen, UserScreen):
            frame = fr(self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.current_screen: tk.Frame = HomeScreen
        self.showHomeScreen()
        self.root.mainloop()

    def showScreen(self, name):
        frame = self.frames[name]
        self.current_screen = frame
        frame.tkraise()

    def showHomeScreen(self):
        self.frames[HomeScreen].initiate_main_display()
        self.showScreen(HomeScreen)

    def showUserScreen(self):
        self.frames[UserScreen].initiate_main_display()
        self.showScreen(UserScreen)

if __name__ == '__main__':
    App()