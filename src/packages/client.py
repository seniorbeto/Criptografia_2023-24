from packages.server import Server, ImgPackage
from packages.imgproc import *
from PIL import Image
from packages.imgproc.img_cripto_utils import ImageCryptoUtils


class Client:
    def __init__(self):
        self.username = None
        self.password = None
        self.encryptor = None
        self.server = Server()

    def get_images(self, num: int | None = -1, username: str | None = None,
                   date: str | None = None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            username (str, optional): name of the camera owner.
                - None it will return all the images from the logged user.
                - "@all" it will return all the images from all the users.
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

        if time is not None:
            if date is None:
                raise Exception("Date must be specified if time is specified")

        if username is None:
            images = self.server.get_images(num=num, username=username, date=date, time=time)
            progress = 0
            for i in images:
                yield round((progress / len(images)) * 100, 2), i
                progress += 1
            return

        # if the user is logged in, we will return de decrypted images
        images = self.server.get_images(num=num, username=username, date=date, time=time)
        decrypted_images = []
        progress = 0
        for im in images:
            decrypted = ImageCryptoUtils.decrypt(im.image, self.password)
            new = ImgPackage(im.author, im.date, im.time, im.path, decrypted)
            decrypted_images.append(new)
            yield round((progress / len(images)) * 100, 2), new
            progress += 1

        return

    def register(self, name: str, password: str) -> None:
        """Creates a new user
        Args:
            name (str): name of the user
            password (str): password of the user
        """

        return self.server.create_user(name, password)

    def logout(self):
        """
        Logs out a user from the server
        :return:
        """
        self.username = None
        self.password = None

    def login(self, name: str, password: str):
        """Logs in a user
        Args:
            name (str): name of the user
            password (str): password of the user
        Returns:
            bool: True if the user was logged in, False otherwise
        """

        if self.server.login(name, password):
            self.username = name
            self.password = password

        else:
            raise ValueError("User or password incorrect")

    def remove_user(self) -> None:
        """Removes the user from the server"""
        if self.server.login(self.username, self.password):
            self.server.remove_user(self.username, self.password)

    def upload_photo(self, path: str, x: int = 0, y: int = 0, w: int = 200, h: int = 200) -> None:
        """Uploads a photo to the server
        Args:
            path (str): path to the image
            x (int, optional): x coordinate of the top left corner of the square to encrypt. Defaults to 0.
            y (int, optional): y coordinate of the top left corner of the square to encrypt. Defaults to 0.
            w (int, optional): width of the square to encrypt. Defaults to 200.
            h (int, optional): height of the square to encrypt. Defaults to 200.
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
        # generate users AES key

        # encrypt image 
        image = ImageCryptoUtils.encrypt(image, self.password, x, y, w, h)
        ImageCryptoUtils.generate_image_hash(image)
        # upload image
        return self.server.store_image(image, self.username, self.password)

    def remove_image(self, date: str, time: str) -> None:
        """Removes the image with the given name
        Args:
            date (str): date of the image
            time (str): time of the image
        """
        return self.server.remove_image(self.username, self.password, date, time)
