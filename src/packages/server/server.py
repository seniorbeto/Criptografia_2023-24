from .user import User
from PIL import Image, PngImagePlugin
from .storage_manager import StorageManager

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
        # generate id for user, this is unique

        users = self.__get_users()
        users.append(User(name, password))
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
        users = self.__get_users()
        for user in users:
            if user.name == name:
                if user.password == password:
                    self.__remove_user(user)
                    return
                else:
                    raise ValueError("Wrong password")
        raise ValueError("User not found")

    def store_image(self, image: Image, user_name):
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
        

        # check if owner is valid
        owner = None
        users = self.__get_users()
        for user in users:
            if user.name == user_name:
                owner = user
                break
        if owner == None:
            raise ValueError("Owner not found")
        
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
        
        for user in users:
            if user.name == name:
                if user.password == password:
                    return True
                else:
                    return False
        return False
    
    def remove_image(self, username: str, date: str, time: str) -> None:
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
        self.__sm.remove_image(username, date, time)

    def clear_server(self):
        """Clears the server
        """
        # REMOVE AFTER TESTING
        self.__sm.delete_all_images()
        self.__sm.delete_all_users()
        self.__sm.create_directories()
        print("Server cleared")