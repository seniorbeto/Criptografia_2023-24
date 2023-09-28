import unittest
from src.packages.api import ServerAPI
import datetime
from freezegun import freeze_time
import os

class TestServerAPI(unittest.TestCase):
    def setUp(self):
        self.api = ServerAPI()
        self.api.server.clear_server()
        self.api.register("user1", "pass1")
        self.api.register("user2", "pass2")
        
    def test_upload_and_get_images(self):
        self.api.login("user1", "pass1")
        self.api.upload_photo("test.png")
        self.api.logout()
        
        self.api.login("user2", "pass2")
        self.api.upload_photo("test.png")
        self.api.logout()
        
        self.api.login("user1", "pass1")
        images = self.api.get_images(10)
        self.assertEqual(len(images), 2)
        self.api.logout()
        
    def test_get_images_by_date(self):
        self.api.login("user1", "pass1")
        self.api.upload_photo("test.png")
        self.api.logout()
        
        self.api.login("user1", "pass1")
        now = datetime.datetime.now()
        images = self.api.get_images(10, date=now.strftime("%Y/%m/%d"))
        self.assertEqual(len(images), 1)
        self.api.logout()
    
    @freeze_time("2022-01-01")
    def test_upload_and_get_images(self):
        self.api.login("user1", "pass1")
        
        # get images from  test_photos folder
        day = 1
        month = 1
        for filename in os.listdir("test_photos"):
            with freeze_time(f"2022-{month}-{day}"):
                self.api.upload_photo("test_photos/" + filename)
                day += 1
                if day%3 == 0:
                    month += 1
        self.api.logout()

        self.api.login("user2", "pass2")
        self.api.upload_photo("test.png")
        self.api.logout()
    


if __name__ == '__main__':
    unittest.main()