import unittest
from packages.api import ServerAPI
import datetime
from freezegun import freeze_time
import os

class TestServerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("SETTING UP SERVER")
        super(TestServerAPI,cls).setUpClass()
        
        cls.api = ServerAPI()
        cls.api.server.clear_server()
        cls.api.register("user1", "pass1")
        cls.api.register("user2", "pass2")
        cls.path = os.path.dirname(os.path.normpath(__file__))
        cls.test_photos = cls.path + "/test_photos/"
        cls.test_png = cls.path + "/test.png"


    def setUp(self) -> None:
        return super().setUp()
    
    def test_login(self):
        print("TESTING LOGIN")
        try:
            self.api.login("user1", "pass1")
            self.api.login("user2", "pass2")
        except Exception as e:
            self.fail(e)
        print("LOGGED IN USERS: 1 y 2")
        
    def test_upload_photo(self):
        print("TESTING UPLOAD PHOTO")
        self.api.login("user1", "pass1")
        self.api.upload_photo(self.test_png)
        self.api.logout()
        print("UPLOADED IMAGE: test.png")

    def test_get_images(self):
        print("TESTING GET IMAGES")
        self.api.login("user1", "pass1")
        self.api.upload_photo(self.test_png)
        self.api.logout()

        self.api.login("user2", "pass2")
        self.api.upload_photo(self.test_png)
        self.api.logout()

        self.api.login("user1", "pass1")
        images = self.api.get_images(2)
        self.assertEqual(len(images), 2)
        self.api.logout()

    
    def test_register_and_login(self):
        print("TESTING REGISTER AND LOGIN")
        self.api.register("test", "test")
        self.api.login("test", "test")
        print("REGISTERED AND LOGGED IN USER: test")

    
    
    @freeze_time("2022-01-01")
    def test_upload(self):
        print("TESTING UPLOAD IMAGES")
        self.api.login("user1", "pass1")
        
        # get images from  test_photos folder
        day = 1
        month = 1
        for filename in os.listdir(self.test_photos):
            with freeze_time(f"2022-{month}-{day}"):
                self.api.upload_photo(self.test_photos + filename)
                day += 1
                if day%3 == 0:
                    month += 1
        
        
        self.api.logout()

        self.api.login("user2", "pass2")
        self.api.upload_photo(self.test_png)
        self.api.logout()
        print("CREATED IMAGES: ")
    
    def test_seach_img_by_author(self):
        print("TESTING SEARCH IMAGE BY AUTHOR")
        self.api.login("user1", "pass1")
        images = self.api.get_images(2)
        print("IMAGES FROM USER1: ", images)
        self.assertEqual(len(images), 2)
        self.api.logout()
        images = self.api.get_images(2, username="user2")
        print("IMAGES FROM USER2: ", images)
        self.assertEqual(len(images), 2)
        self.api.logout()
    
    def test_seach_img_by_date(self):
        date1 = "2022/01/01"
        date2 = "2022/02/03"
        hour1 = "00_00_00"

        self.api.login("user1", "pass1")
        images = self.api.get_images(2, date=date1)
        print("IMAGES FROM DATE user1: ", images)  

        images = self.api.get_images(2, date=date1, username="user2")
        print("IMAGES FROM DATE user2: ", images)

        images = self.api.get_images(2, date=date2, time=hour1)
        print("IMAGES FROM DATE and hour user1: ", images)

        images = self.api.get_images(2, date=date1, time=hour1, username="user2")
        print("IMAGES FROM DATE and hour user2: ", images)





    


def test_seach_img_by_date():
        
        api = ServerAPI()
        date1 = "2022/01/01"
        date2 = "2022/02/03"
        hour1 = "00_00_00"

        api.login("user1", "pass1")
        images = api.get_images(2, date=date1)
        print("IMAGES FROM DATE user1: ", images)  

        images = api.get_images(2, date=date1, username="user2")
        print("IMAGES FROM DATE user2: ", images)

        images = api.get_images(2, date=date2, time=hour1)
        print("IMAGES FROM DATE and hour user1: ", images)

        images = api.get_images(2, date=date1, time=hour1, username="user2")
        print("IMAGES FROM DATE and hour user2: ", images)



        print("TESTING SEARCH IMAGE BY AUTHOR")
        api.login("user1", "pass1")
        images = api.get_images(2)
        print("IMAGES FROM USER1: ", images)
        api.logout()
        images = api.get_images(2, username="user2")
        print("IMAGES FROM USER2: ", images)
        api.logout()

test_seach_img_by_date()
