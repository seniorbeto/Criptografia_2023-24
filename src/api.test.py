import unittest
from packages.api import ServerAPI
import datetime
from freezegun import freeze_time
import os

class TestServerAPI(unittest.TestCase):
    def setUp(self):
        self.api = ServerAPI()
        self.api.server.clear_server()
        self.api.register("user1", "pass1")
        self.api.register("user2", "pass2")
    
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
        self.api.upload_photo("/home/defalco/UNI/Criptografia_2023-24/src/test.png")
        self.api.logout()
        print("UPLOADED IMAGE: /home/defalco/UNI/Criptografia_2023-24/src/test.png")

    def test_get_images(self):
        print("TESTING GET IMAGES")
        self.api.login("user1", "pass1")
        self.api.upload_photo("/home/defalco/UNI/Criptografia_2023-24/src/test.png")
        self.api.logout()

        self.api.login("user2", "pass2")
        self.api.upload_photo("/home/defalco/UNI/Criptografia_2023-24/src/test.png")
        self.api.logout()

        self.api.login("user1", "pass1")
        images = self.api.get_images(2)
        self.assertEqual(len(images), 2)
        self.api.logout()

    
    def register_and_login(self):
        print("TESTING REGISTER AND LOGIN")
        self.api.register("test", "test")
        self.api.login("test", "test")
        print("REGISTERED AND LOGGED IN USER: test")

    
    
    @freeze_time("2022-01-01")
    def test_upload_and_get_images(self):
        print("TESTING UPLOAD AND GET IMAGES")
        self.api.login("user1", "pass1")
        
        # get images from  test_photos folder
        day = 1
        month = 1
        this_path = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(this_path + "/test_photos"):
            with freeze_time(f"2022-{month}-{day}"):
                self.api.upload_photo(this_path+ "/test_photos/" + filename)
                day += 1
                if day%3 == 0:
                    month += 1
        self.api.logout()

        self.api.login("user2", "pass2")
        self.api.upload_photo("/home/defalco/UNI/Criptografia_2023-24/src/test.png")
        self.api.logout()
        print("CREATED IMAGES: ")
    


if __name__ == '__main__':
    unittest.main()