import tkinter as tk
from tkinter import ttk
from screens.home_screen import HomeScreen
from screens.login_toplevel import LoginWindow

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("La pinga de la ponga")
        self.root.configure(highlightthickness=4, highlightcolor="blue")
        self.root.geometry("600x400")

        self.frames = {}
        for fr in (HomeScreen, ):
            frame = fr(self.root)
            self.frames[fr] = frame
            frame.pack(fill=tk.BOTH, expand=True)

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

    def login(self):
        LoginWindow(self.root)

if __name__ == '__main__':
    App()