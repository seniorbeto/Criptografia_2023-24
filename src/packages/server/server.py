from .user import User
from .camera import Camera
import json
import os
import random
from PIL import Image, PngImagePlugin
from time import time

class Server():
    def __init__(self) -> None:
        self.__path = os.path.dirname(os.path.abspath(__file__)) # path to this file
        self.__users = self.__get_users() # list of users
        self.__cameras = self.__get_cameras() # list of cameras

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

    def __get_cameras(self) -> list:
        """Returns the list of cameras
        Returns:
            list: list of cameras
        """
        try:
            with open(f"{self.__path}/data/cameras.json", "r") as file:
                cameras_data = json.load(file)
                # convert data to Camera objects
                cameras = [Camera(**camera_data) for camera_data in cameras_data]

        except:
            cameras = []
        return cameras

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
                      
    def __update_cameras_json(self):
        """Updates the json file with the current cameras
        """
        cameras_data = [camera.__dict__() for camera in self.__cameras]
        with open(f"{self.__path}/data/cameras.json", "w") as file:
            json.dump(cameras_data, file, indent=4)
    
    def __remove_camera(self, camera: Camera) -> None:
        """Removes the given camera
        Args:
            camera (Camera): camera to be removed
        """
        self.__cameras.remove(camera)
        self.__update_cameras_json()

    def create_camera(self, name: str, owner_name:str ) -> None:
        # check if owner is valid
        owner = None
        for user in self.__users:
            if user.name == owner_name:
                owner = user
                break
        if owner == None:
            raise ValueError("Owner not found")
        # check if camera exists
        for camera in self.__cameras:
            if camera.name == name and camera.owner == owner.name:
                raise ValueError("Camera already exists")

        # create camera
        camera = Camera(name = name, owner = owner_name)
        self.__cameras.append(camera)
        # write in file
        self.__update_cameras_json()

    def remove_camera(self, name: str, owner_name: str) -> None:
        # check if owner is valid
        owner = None
        for user in self.__users:
            if user.name == owner_name:
                owner = user
                break
        if owner == None:
            raise ValueError("Owner not found")
        # check if camera exists
        for camera in self.__cameras:
            if camera.name == name and camera.owner == owner.name:
                self.__remove_camera(camera)
                return
        raise ValueError("Camera not found")

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

    def store_image(self, image: Image, camera_name, owner_name):
        """ Stores the image in the server, IMAGE FORMAT: PNG
        Args:
            image_path (str): path to the image 
            camera_name (str): name of the camera
            owner_name (str): name of the owner
        """
        date = int(time())
        # check if owner is valid
        owner = None
        for user in self.__users:
            if user.name == owner_name:
                owner = user
                break
        if owner == None:
            raise ValueError("Owner not found")
            

        # check if camera exists
        
        for camera in self.__cameras:
            if camera.name == camera_name and camera.owner == owner.name:
                break
        else:
            raise ValueError("Camera not found")
        
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
        info.add_text("owner", owner_name)
        info.add_text("camera", camera_name)
        info.add_text("tag", "123456789")
        dest = f"{self.__path}/data/images/{owner_name}/{camera_name}/{date}.png"
        # create directories if they dont exist
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        image.save(dest, "PNG", pnginfo=info)

        print("Image stored with metadata: ", info)

    def get_images(self, num: int, author: str | None = None, camera: str | None=None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the camera owner. Defaults to None.
        Returns:
            list: list of images
        """
        users = [user.name for user in self.__users]

        if author is not None and author not in users:
            raise ValueError("Author not found")

        images = []
        if author is not None and camera is not None:
            return self.__get_images_from_camera(author, camera, num)
        
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
        images = []
        # get random images from random users

        cameras = self.__cameras

        # get just the cameras that have taken a picture
        cameras = [camera for camera in cameras if (camera.owner in os.listdir(f"{self.__path}/data/images") and camera.name in os.listdir(f"{self.__path}/data/images/{camera.owner}"))]

        # get paths of all images

        images_paths = []
        for camera in cameras:
            image_path = f"{self.__path}/data/images/{camera.owner}/{camera.name}"
            images_paths += [f"{image_path}/{image}" for image in os.listdir(image_path)]
        
        # get random images
        num = min(num, len(images_paths))
        
        choices = random.sample(images_paths, k=num)

        for choice in choices:
            images.append(Image.open(choice))
        
        return images
        
    def __get_images_from_camera(self, author: str, camera: str, num: int) -> list:
        """Returns a list of images from the given camera
        Args:
            author (str): name of the author
            camera (str): name of the camera
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
        # check if camera exists
        cameras = [camera.name for camera in self.__cameras]
        if camera not in cameras:
            raise ValueError("Camera not found")
        # check if camera has taken ANY picture = has a path with its name
        if camera not in os.listdir(f"{self.__path}/data/images/{author}"):
            raise ValueError("Camera has no pictures")
        
        
        images = []
        pictures = os.listdir(f"{self.__path}/data/images/{author}/{camera}")
        for picture in pictures:
            if len(images) >= num:
                # there are enough pictures
                return images
            images.append(Image.open(f"{self.__path}/data/images/{author}/{camera}/{picture}"))
        # there are less pictures than num requested
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
        
        images = []
        # get all cameras from author
        author_cameras = [camera for camera in self.__cameras if camera.owner == author]
        # get all cameras from author that have taken a picture
        cameras_with_photos = os.listdir(f"{self.__path}/data/images/{author}")
        
        # get all cameras from author that have taken a picture and are in the cameras list
        # this is to avoid cameras that have been deleted and still have a folder
        cameras = [camera.name for camera in author_cameras if camera.name in cameras_with_photos]

        # get all pictures from all cameras
        for camera in cameras:
            pictures = os.listdir(f"{self.__path}/data/images/{author}/{camera}")
            for picture in pictures:
                if len(images) >= num:
                    # there are enough pictures
                    return images
                images.append(Image.open(f"{self.__path}/data/images/{author}/{camera}/{picture}"))
        # there are less pictures than num requested
        return images

        # for debug
    
    def delete_all_users(self):
        self.__users = []
        self.__update_users_json()
    
    # for debug
    def delete_all_cameras(self):
        self.__cameras = []
        self.__update_cameras_json()

    def delete_all_images(self):
        """Removes directory with all images
        """
        users = os.listdir(f"{self.__path}/data/images")
        for user in users:
            cameras = os.listdir(f"{self.__path}/data/images/{user}")
            for camera in cameras:
                images = os.listdir(f"{self.__path}/data/images/{user}/{camera}")
                for image in images:
                    os.remove(f"{self.__path}/data/images/{user}/{camera}/{image}")
                os.rmdir(f"{self.__path}/data/images/{user}/{camera}")
            os.rmdir(f"{self.__path}/data/images/{user}")
        os.makedirs(f"{self.__path}/data/images", exist_ok=True)

    def clear_server(self):
        self.delete_all_users()
        self.delete_all_cameras()
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

    def get_user_cameras(self, user_name: str) -> list:
        """Returns the list of cameras of the given user
        Args:
            user (User): user
        Returns:
            list: list of cameras
        """
        # check if user exists
        users = [user.name for user in self.__users]
        if user_name not in users:
            raise ValueError("User not found")

        return [camera.name for camera in self.__cameras if camera.owner == user_name]