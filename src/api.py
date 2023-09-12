from packages.system import *

class ServerAPI():
    def __init__(self):
        self.server = Server()

    def getCameraImages(self, *args, **kwargs):
        return self.server.get_camera_images(*args, **kwargs)
