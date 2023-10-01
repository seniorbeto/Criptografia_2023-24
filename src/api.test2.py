from packages.api import ServerAPI
import tracemalloc
import os
import freezegun
from PIL import Image
tracemalloc.start()
api = ServerAPI()

api.login("user1", "pass1")
print(api.get_images(username="@all"))

