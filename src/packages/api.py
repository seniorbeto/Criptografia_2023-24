from packages.server import Server
from PIL import Image

class ServerAPI():
    def __init__(self):
        self.username = None
        self.password = None
        self.server = Server()

    def get_images(self, num: int | None = -1, username: str | None = None, 
                   date:str | None = None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the camera owner. Defaults to None.
            date (str, optional): date of the images. Defaults to None.ç
                format: "%Y/%m/%d"

            time (str, optional): time of the images. Defaults to None.
                format: HH_MM_SS
        Returns:
            list: list of images
        """
        # si no se espècifica usuario se coge al usuario logeado (si hay, si no sera None)
        if username is None:
            username = self.username
        # si se especifica @all se coge todas las imagenes idependientemente del usuario logeado
        if username == "@all":
            username = None
        
        if date is not None:
            author = self.username
        if time is not None:
            if date is None:
                raise Exception("Date must be specified if time is specified")

        return self.server.get_images(num=num, username=username, date = date, time = time)
    
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
            raise ValueError("User or password incorrect")

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
        except Exception as e:
            print(e)
            raise Exception("Image could not be opened check path and format")
        # encrypt image
        # TODO
        # upload image
        return self.server.store_image(image, self.username)
    
    def remove_image(self, date: str, time: str) -> None:
        """Removes the image with the given name
        Args:
            date (str): date of the image
            time (str): time of the image
        """
        return self.server.remove_image(self.username, date, time)