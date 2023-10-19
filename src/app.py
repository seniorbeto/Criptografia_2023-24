import tkinter as tk
from tkinter import ttk
from screens.home_screen import HomeScreen
from screens.user_screen import UserScreen
from screens.loading_screen import LoadingScreen
from packages.client import Client

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.api = Client()
        self.root.title("La pinga de la ponga")
        self.root.geometry("700x400")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.user = None

        self.loading_progress = 0

        self.frames = {}
        for fr in (HomeScreen, UserScreen, LoadingScreen):
            frame = fr(self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.current_screen: tk.Frame = HomeScreen
        self.showHomeScreen()
        self.root.mainloop()

    def resetProgress(self):
        self.loading_progress = 0
        self.frames[LoadingScreen].progress_bar["value"] = 0
        self.frames[LoadingScreen].update()

    def updateProgress(self, progress):
        self.loading_progress = progress
        self.frames[LoadingScreen].progress_bar["value"] = progress
        self.frames[LoadingScreen].update()

    def updateStatus(self, status):
        self.frames[LoadingScreen].update_status(status)

    def showScreen(self, name):
        frame = self.frames[name]
        self.current_screen = frame
        frame.tkraise()

    def showHomeScreen(self):
        self.frames[LoadingScreen].initiate_main_display()
        self.showScreen(LoadingScreen)
        self.root.after(100, self.__showHomeScreen)

    def __showHomeScreen(self):
        self.frames[HomeScreen].initiate_main_display()
        self.showScreen(HomeScreen)

    def showUserScreen(self):
        self.frames[LoadingScreen].initiate_main_display()
        self.showScreen(LoadingScreen)
        self.root.after(100, self.__showUserScreen)

    def __showUserScreen(self):
        self.frames[UserScreen].initiate_main_display()
        self.showScreen(UserScreen)

if __name__ == '__main__':
    App()