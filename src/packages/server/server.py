from .user import User
from PIL import Image, PngImagePlugin
from .storage_manager import StorageManager
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt  import Scrypt
import re
import uuid


class Server():
    def __init__(self) -> None:
        self.__sm = StorageManager()
        self.__sm.create_directories()

    def __get_users(self) -> list:
        """Returns the list of users
        Returns:
            list: list of users
        """
        return self.__sm.get_users()

    def __remove_user(self, user: User) -> None:
        """Removes the given user
        Args:
            user (User): user to be removed
        """
        users = self.__get_users()
        users.remove(user)
        self.__sm.update_users_json(users)
    


    def create_user(self, name, password) -> None:
        """Creates a new user with the given name and password
        Args:
            name (str): name of the user
            password (str): password of the user (hashed)
        """
        # check if name is unique
        users = self.__get_users()
        for user in users:
            if user.name == name:
                raise ValueError("Name is already taken")
            
        
        # TODO la contraseña estara encriptada con RSA y el servidor tendra la clave privada
        # TODO desencriptar la contraseña con la clave privada del servidor
        
        #  check if password is hashed 256
        sha256 = re.compile(r"^[a-fA-F0-9]{64}$")
        if not sha256.match(password):
            raise ValueError("Password is not hashed with SHA256")
        
        # KDF de la contraseña
        # TODO
        salt = uuid.uuid4().hex
        kdf = Scrypt(
            salt = bytes.fromhex(salt),
            length = 32,
            n = 2**14,
            r = 8,
            p = 1
        )
        password = kdf.derive(bytes.fromhex(password)).hex()


        # create user
        users = self.__get_users()
        users.append(User(name, password, salt))
        self.__sm.update_users_json(users)
        
    def remove_user(self, name: str, password: str):
        """Removes the user with the given name
        Args:
            name (str): name of the user
            password (str): password of the user (hashed)
        """
        print("Trying to remove: ", name, " ", password)
        if name == "":
            raise ValueError("Name cannot be empty")
        elif password == "":
            raise ValueError("Password cannot be empty")
        
        # check if user exists and if password is correct
        if self.__check_password(name=name, password=password):
            pass
        raise ValueError("User not found")

    def store_image(self, image: Image, user_name, password):
        """ Stores the image in the server, IMAGE FORMAT: PNG
        Args:
            image_path (str): path to the image 
            camera_name (str): name of the camera
            user_name (str): name of the owner
        """
        if user_name == "" or user_name is None:
            raise ValueError("User cannot be empty")
        if image is None:
            raise ValueError("Image cannot be empty")
        

        # check if owner is valid and if password is correct
        if not self.__check_password(user_name, password):
            raise ValueError("User or password incorrect")
        
        
        # checK  tags #TODO
        pass
        # check signature #TODO
        pass
        # check certificate #TODO
        pass
        # store image 
        
        # dev and debug purposes
        image.load()

        # META DATA
        # copy metadata from original image to new image
        info = PngImagePlugin.PngInfo()
        for key, value in image.info.items():
            info.add_text(str(key), str(value))
        # add new metadata
        info.add_text("sample tag", "1234")
        
        # store image
        self.__sm.storage_img(image, user_name, info)
    
    def get_images(self, num: int, username: str | None = None, date: str | None =None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the  owner. Defaults to None.
            date (str, optional): date of the images. Defaults to None.
                format: "%Y/%m/%d"
            time (str, optional): time of the images. Defaults to None.
                format: HH_MM_SS
        Returns:
            list: list of images
        """
        # CHECKS #TODO

        # get images
        return self.__sm.get_images(num, username, date, time)

    def login(self, name: str, password: str) -> bool:
        """Logs in a user
        Args:
            name (str): name of the user
            password (str): password of the user
        Returns:
            bool: True if the user was logged in, False otherwise
        """
        # update users
        users = self.__get_users()

        # check if user exists
        usernames = [ user.name for user in users ]
        if name not in usernames:
            return False
        
        # check if password is correct
        return self.__check_password(name, password)
    
    def remove_image(self, username: str, password:str, date: str, time: str) -> None:
        """Removes the image with the given name
        Args:
            username (str): name of the user
            date (str): date of the image
            time (str): time of the image
        """
        if username == "" or username is None:
            raise ValueError("Username cannot be empty")
        elif date == "":
            raise ValueError("Date cannot be empty")
        elif time == "":
            raise ValueError("Time cannot be empty")
        
        if not self.__check_password(username, password):
            raise ValueError("User or password incorrect")
        
        self.__sm.remove_image(username, date, time)

    
    def __check_password(self, name: str, password: str) -> bool:
        # get users salt and password
        users = self.__get_users()
        for user in users:
            if user.name == name:
                # generate kdf with salt
                kdf = Scrypt(
                    salt = bytes.fromhex(user.salt),
                    length = 32,
                    n = 2**14,
                    r = 8,
                    p = 1
                )
                password = kdf.derive(bytes.fromhex(password)).hex()
                if user.password == password:
                    return True
                else:
                    return False
        return False
    
    def clear_server(self):
        """Clears the server
        """
        # REMOVE AFTER TESTING
        self.__sm.delete_all_images()
        self.__sm.delete_all_users()
        self.__sm.create_directories()
        print("Server cleared")