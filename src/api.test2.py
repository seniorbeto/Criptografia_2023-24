from packages.api import ServerAPI
import tracemalloc
import os
import freezegun
from PIL import Image
tracemalloc.start()
api = ServerAPI()

api.login("user1", "pass1")
print(api.get_images(username="@all"))

# api.remove_image("2022/02/05", "00_00_00")
api.remove_image("2022/02/04", "00_00_00")
api.remove_image("2022/02/03", "00_00_00")