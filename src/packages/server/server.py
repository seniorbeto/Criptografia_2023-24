from .user import User
import json
import os
import random
from PIL import Image, PngImagePlugin
from datetime import datetime

class Server():
    def __init__(self) -> None:
        self.__path = os.path.dirname(os.path.abspath(__file__)) # path to this file
        self.__users = self.__get_users() # list of users
        self.__create_directories()

    def __create_directories(self) -> None:
        """Creates the directories needed for the server to work
        """
        # create directories if they dont exist
        os.makedirs(f"{self.__path}/data", exist_ok=True)
        os.makedirs(f"{self.__path}/data/images", exist_ok=True)

    def __get_users(self) -> list:
        """Returns the list of users
        Returns:
            list: list of users
        """
        try:
            with open(f"{self.__path}/data/users.json", "r") as file:
                users_data = json.load(file)
                # convert data to User objects
                users = [User(**user_data) for user_data in users_data]
        except:
            print("Error reading users.json")
            users = []
        return users

    def __remove_user(self, user: User) -> None:
        """Removes the given user
        Args:
            user (User): user to be removed
        """
        self.__users.remove(user)
        self.__update_users_json()
    
    def __update_users_json(self):
        """Updates the json file with the current users
        """
        users_data = [user.__dict__() for user in self.__users]
        with open(f"{self.__path}/data/users.json", "w") as file:
            json.dump(users_data, file, indent=4)

    def create_user(self, name, password) -> None:
        """Creates a new user with the given name and password
        Args:
            name (str): name of the user
            password (str): password of the user (hashed)
        """

        # check if name is unique
        for user in self.__users:
            if user.name == name:
                raise ValueError("Name is already taken")
        # generate id for user, this is unique

        user = User(name = name, password = password)
        self.__users.append(user)
        # write in file
        self.__update_users_json()
        
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
        
        for user in self.__users:
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

        now = datetime.now()
        date = now.strftime("%Y/%m/%d")
        time = now.strftime("%H_%M_%S")
        # check if owner is valid
        owner = None
        for user in self.__users:
            if user.name == user_name:
                owner = user
                break
        if owner == None:
            raise ValueError("Owner not found")
        
        # chekc  tags #TODO
        pass
        # check signature #TODO
        pass
        # check certificate #TODO
        pass
        # store image 
        
        # dev and debug purposes
        image.load()
        info = PngImagePlugin.PngInfo()
        # copy metadata from original image to new image
        for key, value in image.info.items():
            info.add_text(str(key), str(value))
        # add new metadata
        info.add_text("owner", user_name)
        info.add_text("tag", "123456789")
        dest = f"{self.__path}/data/images/{user_name}/{date}/{time}.png"
        # create directories if they dont exist
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        image.save(dest, "PNG", pnginfo=info)

        print("Image stored with metadata: ", info)

    def get_images(self, num: int, author: str | None = None, date: str | None =None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the  owner. Defaults to None.
            date_time (str, optional): date and time of the image. Defaults to None.
                format: "%Y/%m/%d" HH_MM_SS 
        Returns:
            list: list of images
        """
        if num <= 0 or num is None:
            num = float("inf")
        users = [user.name for user in self.__users]
        images = []

        if author is not None and author not in users:
            raise ValueError("Author not found")
        
        if author is not None and date is not None:
            return self.__get_images_from_date(author, date, time, num)
        if author is None and date is not None:
            raise ValueError("Date must be specified with author")

        elif author is not None:
            return self.__get_images_from_author(author, num)

        else:
            return self.__get_random_images(num)
            
    def __get_random_images(self, num: int) -> list:
        """Returns a list of random images
        Args:
            num (int): number of images to return
        Returns:
            list: list of images
        """
        # get random images from random users


        # get just the cameras that have taken a picture
        # get paths of all images 
        # path has format: data/images/author/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []
        for user in self.__users:
            years = os.listdir(f"{self.__path}/data/images/{user.name}")
            for year in years:
                months = os.listdir(f"{self.__path}/data/images/{user.name}/{year}")
                for month in months:
                    days = os.listdir(f"{self.__path}/data/images/{user.name}/{year}/{month}")
                    for day in days:
                        images_paths += [f"{self.__path}/data/images/{user.name}/{year}/{month}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{user.name}/{year}/{month}/{day}")]
        
        # get random images
        num = min(num, len(images_paths))
        
        choices = random.sample(images_paths, k=num)

        images = []
        for choice in choices:
            images.append(Image.open(choice))
        
        return images
        

    def __get_images_from_author(self, author: str, num: int) -> list:
        """Returns a list of images from the given author
        Args:
            author (str): name of the author
            num (int): number of images to return if -1 returns all images
        Returns:
            list: list of images
        """
        if num == -1:
            num = float("inf")
        
        # check if author exists
        users = [user.name for user in self.__users]
        if author not in users:
            raise ValueError("Author not found")
        # check if author has taken ANY picture = has a path with his name
        if author not in os.listdir(f"{self.__path}/data/images"):
            raise ValueError("Author has no pictures")
        
        # get paths of all images
        # path has format: data/images/author/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []
        years = os.listdir(f"{self.__path}/data/images/{author}")
        for year in years:
            months = os.listdir(f"{self.__path}/data/images/{author}/{year}")
            for month in months:
                days = os.listdir(f"{self.__path}/data/images/{author}/{year}/{month}")
                for day in days:
                    images_paths += [f"{self.__path}/data/images/{author}/{year}/{month}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{author}/{year}/{month}/{day}")]
        
        # get random images
        num = min(num, len(images_paths))

        choices = random.sample(images_paths, k=num)

        images = []
        for choice in choices:
            images.append(Image.open(choice))
        
        return images

    def __get_images_from_date(self, author: str, date: str, time:str = None, num: int = None) -> list:
        """Returns a list of images from the given author and date
        Args:
            author (str): name of the author
            date (str): date of the image - format: YYYY/MM/DD
            time (str): time of the image - format: HH_MM_SS
            num (int): number of images to return if -1 returns all images
        Returns:
            list: list of images
        """
        if num == -1:
            num = float("inf")
        
        # check if author exists
        users = [user.name for user in self.__users]
        if author not in users:
            raise ValueError("Author not found")
        # check if author has taken ANY picture = has a path with his name
        if author not in os.listdir(f"{self.__path}/data/images"):
            raise ValueError("Author has no pictures")
        
        # get paths of all images
        # path has format: data/images/author/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []

        #try to get images from date

        try:
            images_paths += [f"{self.__path}/data/images/{author}/{date}/{image}" for image in os.listdir(f"{self.__path}/data/images/{author}/{date}")]

        except:
            # date not found
            raise ValueError("Date not found")

        # try to get images from time
        if time is not None:
            try:
                return [Image.open(f"{self.__path}/data/images/{author}/{date}/{time}.png")]
            except:
                # time not found
                raise ValueError("Time not found")
        

        # get random images
        num = min(num, len(images_paths))

        choices = random.sample(images_paths, k=num)

        images = []
        for choice in choices:
            images.append(Image.open(choice))
        
        return images


    
    def delete_all_users(self):
        self.__users = []
        self.__update_users_json()


    def delete_all_images(self):
        """Removes directory with all images
        """
        
        users = os.listdir(f"{self.__path}/data/images")
        for user in users:
            years = os.listdir(f"{self.__path}/data/images/{user}")
            for year in years:
                months = os.listdir(f"{self.__path}/data/images/{user}/{year}")
                for month in months:
                    days = os.listdir(f"{self.__path}/data/images/{user}/{year}/{month}")
                    for day in days:
                        images = os.listdir(f"{self.__path}/data/images/{user}/{year}/{month}/{day}")
                        for image in images:
                            os.remove(f"{self.__path}/data/images/{user}/{year}/{month}/{day}/{image}")
                        os.rmdir(f"{self.__path}/data/images/{user}/{year}/{month}/{day}")
                    os.rmdir(f"{self.__path}/data/images/{user}/{year}/{month}")
                os.rmdir(f"{self.__path}/data/images/{user}/{year}")
            os.rmdir(f"{self.__path}/data/images/{user}")
        os.rmdir(f"{self.__path}/data/images")

    def clear_server(self):
        self.delete_all_users()
        self.delete_all_images()

    def login(self, name: str, password: str) -> bool:
        """Logs in a user
        Args:
            name (str): name of the user
            password (str): password of the user
        Returns:
            bool: True if the user was logged in, False otherwise
        """
        for user in self.__users:
            if user.name == name:
                if user.password == password:
                    return True
                else:
                    return False
        return False
