from .packages.server import Server
from PIL import Image

class ServerAPI():
    def __init__(self):
        self.server = Server()

    def get_images(self, num: int, author: str | None = None, camera: str | None=None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the camera owner. Defaults to None.
        Returns:
            list: list of images
        """
        return self.server.get_images(num, author, camera)
    
    def create_camera(self, name: str, owner_name: str) -> None:
        """Creates a new camera
        Args:
            name (str): name of the camera
            author (str): name of the camera owner
        """
        return self.server.create_camera(name, owner_name)
    
    def remove_camera(self, name: str, owner_name: str):
        """Removes a camera
        Args:
            name (str): name of the camera
            author (str): name of the camera owner
        """
        return self.server.remove_camera(name, owner_name)
    
    def create_user(self, name: str, password: str) -> None:
        """Creates a new user
        Args:
            name (str): name of the user
            password (str): password of the user
        """
        return self.server.create_user(name, password)
    
    def login(self, name: str, password: str) -> bool:
        """Logs in a user
        Args:
            name (str): name of the user
            password (str): password of the user
        Returns:
            bool: True if the user was logged in, False otherwise
        """
        #TODO
        """
        habra que hacer una funcion que verifique si los datos son correctos
        o igual no es necesario un login, depende de la implementacion que 
        hagamos de la seguridad 
        """
        pass 

    def upload_photo(self, path: str, camera: str, author: str) -> None:
        """Uploads a photo to the server
        Args:
            path (str): path to the image MUST BE A PNG
            camera (str): name of the camera that took the image
            author (str): name of the camera owner
        """ 
        # check if image is png
        if not path.endswith(".png"):
            raise Exception("Image must be a PNG")
        # try to open image
        try:
            image = Image.open(path)
        except:
            raise Exception("Image could not be opened check path and format")

        return self.server.store_image(image, camera, author)