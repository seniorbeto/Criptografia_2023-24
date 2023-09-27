import tkinter as tk

class AdminScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.app = app

    def initiate_main_display(self):
        """
        We make this method so that the frame itself is not created until the user is logged in
        """
        # We create a canvas to put the scrollbar in it
        # Calculate de height that the menu is taking
        menu_height = self.app.main_menu.winfo_height()
        self.canvas = tk.Canvas(self, background="#212121", highlightthickness=0, borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=menu_height)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=menu_height)

        # We configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.canvas_reconfigure)

        self.show_cameras()
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def canvas_reconfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_cameras(self):
        # If the user is not logged in it will raise an exception
        user_cameras = self.app.api.get_cameras()

        i = 0
        for cam in user_cameras:
            new_frame = tk.Frame(self.canvas, background="#454545")
            self.canvas.create_window((0, i*70), window=new_frame, anchor=tk.CENTER, width=300)
            i += 1
            """
            In this new frame, we will include de camera name and the delete button 
            """
            tk.Label(new_frame, text=cam, background="#454545", foreground="#ffffff").pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(new_frame, text="Delete", command=lambda camera=cam: self.delete_camera(camera)).pack(side=tk.RIGHT, padx=10, pady=10)
            tk.Button(new_frame, text="Show Images", command=lambda: self.show_images(cam)).pack(side=tk.RIGHT, padx=10, pady=10)

    def delete_camera(self, cam):
        print("Deleting camera", cam)
        self.app.api.remove_camera(cam)
        # We destroy the frame and create it again so it refreshes
        self.refresh()

    def show_images(self, cam):...

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self.initiate_main_display()
