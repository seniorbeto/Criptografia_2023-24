import tkinter as tk
from tkinter import messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.geometry("200x300")
        self.title("Login")
        self.app = app

        # Username
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack(padx=10, pady=15)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=10, pady=15)

        # Password
        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack(padx=10, pady=15)
        self.password_entry = tk.Entry(self)
        self.password_entry.pack(padx=10, pady=15)

        #############################
        button = tk.Button(self, text="APAÑAO", command=self.check_login)
        button.pack(padx=10, pady=30)

    def check_login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "admin":
            self.destroy()
            self.app.enable_admin_mode()
        else:
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            messagebox.showerror("Error", "AY SEÑORA VACA METEMO QUE NONONONONONO")