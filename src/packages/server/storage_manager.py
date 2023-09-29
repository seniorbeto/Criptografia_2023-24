import os
import json
from .user import User
from PIL import Image
from datetime import datetime
import random
import re

class StorageManager():
    def __init__(self) -> None:
        self.__path = os.path.dirname(os.path.abspath(__file__)) # path to this file

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
        path = f"{self.__path}/data/images/{username}/{now.year}/{now.month}/{now.day}/{now.hour}_{now.minute}_{now.second}.png"
        
        # create directories if they dont exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, "PNG", pnginfo=metadata)
    
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
        users = os.listdir(f"{self.__path}/data/images")
        for user in users:
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
        
        # check if author has taken ANY picture = has a path with his name
        if author not in os.listdir(f"{self.__path}/data/images"):
            raise ValueError("Author has no pictures")
        
        # get paths of all images
        # path has format: data/images/author/YYYY/MM/DD/hh_mm_ss.png
        images_paths = []

        # In order to get images from date we need to check if the date given is only a year, a year and a month or a year, month and day
        # We do that by converting the string into a tuple of ints whose length varies depending on the date given. For example,
        # if the date given is 2021/05/12, the tuple will be (2021, 5, 12). If the date given is 2021/05, the tuple will be (2021, 5), etc.
        new_date = self.__load_date(date)
        if len(new_date) == 3:
            try:
                images_paths += [f"{self.__path}/data/images/{author}/{date}/{image}" for image in os.listdir(f"{self.__path}/data/images/{author}/{date}")]
            except:
                # date not found
                raise ValueError("Date not found")
        elif len(new_date) == 2:
            try:
                days = os.listdir(f"{self.__path}/data/images/{author}/{new_date[0]}/{new_date[1]}")
                for day in days:
                    images_paths += [f"{self.__path}/data/images/{author}/{new_date[0]}/{new_date[1]}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{author}/{new_date[0]}/{new_date[1]}/{day}")]
            except:
                # date not found
                raise ValueError("Date not found")
        elif len(new_date) == 1:
            try:
                months = os.listdir(f"{self.__path}/data/images/{author}/{new_date[0]}")
                for month in months:
                    days = os.listdir(f"{self.__path}/data/images/{author}/{new_date[0]}/{month}")
                    for day in days:
                        images_paths += [f"{self.__path}/data/images/{author}/{new_date[0]}/{month}/{day}/{image}" for image in os.listdir(f"{self.__path}/data/images/{author}/{new_date[0]}/{month}/{day}")]
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
