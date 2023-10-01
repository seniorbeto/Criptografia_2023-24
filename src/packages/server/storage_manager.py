import os
import json
from .user import User
from PIL import Image
from datetime import datetime
import random
import re

class StorageManager():
    def __init__(self) -> None:
        self.__path = os.path.dirname(os.path.normpath(__file__)) # path to this file

    def create_directories(self) -> None:
        """Creates the directories needed for the server to work
        """
        # create directories if they dont exist
        os.makedirs(f"{self.__path}/data", exist_ok=True)
        os.makedirs(f"{self.__path}/data/images", exist_ok=True)
    

    def get_users(self) -> list:
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

    def update_users_json(self, users: list) -> None:
        """
        Updates the json file with the current users
        """
        users_data = [user.__dict__() for user in users]
        with open(f"{self.__path}/data/users.json", "w") as file:
            json.dump(users_data, file, indent=4)
    
    def storage_img(self, img: Image, username:str, metadata) -> None:
        """Stores an image
        Args:
            img (bytes): image
            name (str): name of the image
            metadata (dict): metadata of the image
        """
        # save image
        # calculate path: images/username/yyyy/mm/dd/hour_minute_second.png
        now = datetime.now()

        year = now.year
        month = f"0{now.month}" if now.month < 10 else now.month
        day = f"0{now.day}" if now.day < 10 else now.day
        hour = f"0{now.hour}" if now.hour < 10 else now.hour
        minute = f"0{now.minute}" if now.minute < 10 else now.minute
        second = f"0{now.second}" if now.second < 10 else now.second

        path = f"{self.__path}/data/images/{username}/{year}/{month}/{day}/{hour}_{minute}_{second}.png"
        
        # create directories if they dont exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, "PNG", pnginfo=metadata)
    
    def get_images(self, num: int, username: str | None = None, date: str | None =None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            username (str, optional): name of the  owner. Defaults to None.
            date (str, optional): date of the images. Defaults to None.
                format: "%Y/%m/%d"
            time (str, optional): time of the images. Defaults to None.
                format: HH_MM_SS
        Returns:
            list: list of images
        """

        
        if username is not None and date is not None:
            return self.__get_images_from_date(username, date, time, num)
        if username is None and date is not None:
            raise ValueError("Date must be specified with username")

        elif username is not None:
            return self.__get_images_from_username(username, num)

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
        # path has format: data/images/username/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []
        users = os.listdir(f"{self.__path}/data/images")
        for user in users:
            years = os.listdir(f"{self.__path}/data/images/{user}")
            for year in years:
                months = os.listdir(f"{self.__path}/data/images/{user}/{year}")
                for month in months:
                    days = os.listdir(f"{self.__path}/data/images/{user}/{year}/{month}")
                    for day in days:
                        images_paths += [f"{self.__path}/data/images/{user}/{year}/{month}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{user}/{year}/{month}/{day}")]
        
        # get random images
        num = min(num, len(images_paths))
        
        choices = random.sample(images_paths, k=num)

        images = []
        for choice in choices:
            images.append(Image.open(choice))
        
        return images
        

    def __get_images_from_username(self, username: str, num: int) -> list:
        """Returns a list of images from the given username
        Args:
            username (str): name of the username
            num (int): number of images to return if -1 returns all images
        Returns:
            list: list of images
        """
        if num == -1:
            num = float("inf")
        # check if username has taken ANY picture = has a path with his name
        if username not in os.listdir(f"{self.__path}/data/images"):
            raise ValueError("username has no pictures")
        
        # get paths of all images
        # path has format: data/images/username/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []
        years = os.listdir(f"{self.__path}/data/images/{username}")
        for year in years:
            months = os.listdir(f"{self.__path}/data/images/{username}/{year}")
            for month in months:
                days = os.listdir(f"{self.__path}/data/images/{username}/{year}/{month}")
                for day in days:
                    images_paths += [f"{self.__path}/data/images/{username}/{year}/{month}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{username}/{year}/{month}/{day}")]
        
        # get random images
        num = min(num, len(images_paths))

        choices = random.sample(images_paths, k=num)

        images = []
        for choice in choices:
            images.append(Image.open(choice))
        
        return images

    def __get_images_from_date(self, username: str, date: str, time:str = None, num: int = None) -> list:
        """Returns a list of images from the given username and date
        Args:
            username (str): name of the username
            date (str): date of the image - format: YYYY/MM/DD
            time (str): time of the image - format: HH_MM_SS
            num (int): number of images to return if -1 returns all images
        Returns:
            list: list of images
        """
        if num == -1:
            num = float("inf")
        
        # check if username has taken ANY picture = has a path with his name
        if username not in os.listdir(f"{self.__path}/data/images"):
            raise ValueError("username has no pictures")
        
        # get paths of all images
        # path has format: data/images/username/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []

        # In order to get images from date we need to check if the date given is only a year, a year and a month or a year, month and day
        # We do that by converting the string into a tuple of ints whose length varies depending on the date given. For example,
        # if the date given is 2021/05/12, the tuple will be (2021, 5, 12). If the date given is 2021/05, the tuple will be (2021, 5), etc.
        new_date = self.__load_date(date)
        if len(new_date) == 3:
            try:
                images_paths += [f"{self.__path}/data/images/{username}/{date}/{image}" for image in os.listdir(f"{self.__path}/data/images/{username}/{date}")]
            except:
                # date not found
                raise ValueError("Date not found")
        elif len(new_date) == 2:
            try:
                days = os.listdir(f"{self.__path}/data/images/{username}/{new_date[0]}/{new_date[1]}")
                for day in days:
                    images_paths += [f"{self.__path}/data/images/{username}/{new_date[0]}/{new_date[1]}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{username}/{new_date[0]}/{new_date[1]}/{day}/")]
            except:
                # date not found
                raise ValueError("Date not found")
        elif len(new_date) == 1:
            try:
                months = os.listdir(f"{self.__path}/data/images/{username}/{new_date[0]}")
                for month in months:
                    days = os.listdir(f"{self.__path}/data/images/{username}/{new_date[0]}/{month}")
                    for day in days:
                        images_paths += [f"{self.__path}/data/images/{username}/{new_date[0]}/{month}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{username}/{new_date[0]}/{month}/{day}")]
            except:
                # date not found
                raise ValueError("Date not found")


        # try to get images from time
        if time is not None:
            try:
                return [Image.open(f"{self.__path}/data/images/{username}/{date}/{time}.png")]
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

    def __load_date(self, date: str) -> tuple[int, int, int]:
        """
        Loads a date from a string with format YYYY/MM/DD and converts it to a tuple of ints
        """
        pattern = r'^(\d{4})(/(\d{2})(/(\d{2}))?)?$'
        if not re.match(pattern, date):
            raise ValueError("Invalid date format")

        return tuple(date.split("/"))
    
    def delete_all_users(self):
        # REMOVE AFTER TESTING
        self.update_users_json([])


    def delete_all_images(self):
        """Removes directory with all images
        """
        # REMOVE AFTER TESTING
        
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
