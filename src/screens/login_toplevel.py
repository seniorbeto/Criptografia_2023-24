import tkinter as tk

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("200x300")
        self.title("Login")

        #############################
        button = tk.Button(self, text="APAÑAO", command=self.check_login)
        button.pack()

    def check_login(self):
        pass