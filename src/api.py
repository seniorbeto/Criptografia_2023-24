from .packages.server import Server
from PIL import Image

class ServerAPI():
    def __init__(self):
        self.username = None
        self.password = None
        self.server = Server()

    def get_images(self, num: int, author: str | None = None, 
                   time:str | None = None, date:str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the camera owner. Defaults to None.
        Returns:
            list: list of images
        """
        return self.server.get_images(num=num, author=author, date = date, time = time)
    
    def register(self, name: str, password: str) -> None:
        """Creates a new user
        Args:
            name (str): name of the user
            password (str): password of the user
        """
        # TODO
        return self.server.create_user(name, password)

    def logout(self):
        """
        Logs out a user from the server
        :return:
        """
        self.username = None
        self.password = None

    def get_cameras(self) -> list:
        return self.server.get_user_cameras(self.username)

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
        if self.server.login(name, password):
            self.username = name
            self.password = password
        else:
            raise Exception("User or password incorrect")

    def upload_photo(self, path: str) -> None:
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
        # encrypt image
        # TODO
        # upload image
        return self.server.store_image(image, self.username)