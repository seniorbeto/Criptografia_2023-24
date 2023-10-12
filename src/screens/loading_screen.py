import tkinter as tk

class LoadingScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#525252")
        self.app = app

    def initiate_main_display(self):
        # First, if the frame is not empty, we destroy all the widgets
        for w in self.winfo_children():
            w.destroy()

        # Eliminate the menu
        self.app.root.config(menu=None)

        # Loading label
        self.loading_label = tk.Label(self, text="Loading...", background="#525252",
                                      foreground="#ffffff", font="Helvetica 20 bold")
        self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

if __name__ == '__main__':
    class appTest:
        def __init__(self):
            self.root = tk.Tk()
            self.root.geometry("700x400")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.frames = {}
            for fr in (LoadingScreen,):
                frame = fr(self)
                self.frames[fr] = frame
                frame.grid(row=0, column=0, sticky=tk.NSEW)
            self.current_screen: tk.Frame = LoadingScreen
            self.showLoadingScreen()
            self.root.mainloop()

        def showScreen(self, name):
            frame = self.frames[name]
            self.current_screen = frame
            frame.tkraise()

        def showLoadingScreen(self):
            self.frames[LoadingScreen].initiate_main_display()
            self.showScreen(LoadingScreen)

    appTest()