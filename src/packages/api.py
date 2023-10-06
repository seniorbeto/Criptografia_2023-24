from packages.server import Server
from packages.imgproc import *
from PIL import Image
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import json

class ServerAPI():
    def __init__(self):
        self.username = None
        self.password = None
        self.encryptor = None
        self.server = Server()

    def get_images(self, num: int | None = -1, username: str | None = None, 
                   date:str | None = None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the camera owner.
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

        if self.server.login(name, password):
            self.username = name
            self.password = password

        else:
            raise ValueError("User or password incorrect")

    def get_salt_k(self) -> bytes:
        """Returns the salt key of the user
        Returns:
            bytes: salt key
        """
        salt_k = self.server.get_salt_k(self.username)
        return bytes.fromhex(salt_k) 
    

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
        # generate aes key
        key = PBKDF2HMAC(
            salt = self.get_salt_k(),
            length = 192,
            algorithm=hashes.SHA256(),
            iterations=100000
        ).derive(self.password.encode())
        # encrypt image with aes
        init_vector = b'\x12\x97\x9f\xd2\xd8\xac_\n2\x134=\x07\xea=\xd7'

        cipher = Cipher(algorithms.AES(key), modes.CBC(init_vector))
        self.__encryptor = cipher.encryptor()

        pixels = getColors(image, x=50, y=50, width=100, height=100)
        new_pixels = []
        for px in pixels:
            print(pixels[px].strip("#"))
            new = self.__encryptor.update(bytes.fromhex(pixels[px].strip("#")))
            if str(new.hex()) == "":
                new_pixels.append("#"+str(new.hex()))
            print("#"+str(new.hex()))
        updatePixels(image, x=50, y=50, width=100, height=100, color=new_pixels)

        # upload image
        return self.server.store_image(image, self.username, self.password)
    
    def remove_image(self, date: str, time: str) -> None:
        """Removes the image with the given name
        Args:
            date (str): date of the image
            time (str): time of the image
        """
        return self.server.remove_image(self.username, self.password, date, time)

    def remove_user(self) -> None:
        """Removes the user from the server"""
        return self.server.remove_user(self.username)

    def update_local_json(self):
        """Updates the json file"""
        json_data = {
            "username": self.username,
            "password": self.password,
            "encryptor": self.encryptor
        }
        with open("data.json", "w") as json_file:
            json.dump("local_user_data.json", json_file)
        