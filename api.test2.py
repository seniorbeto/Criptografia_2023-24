from src.packages.api import ServerAPI
import datetime
from freezegun import freeze_time
import os

api = ServerAPI()

api.login("user1", "pass1")

api.get_images(date="2022/01/01")[0].show()