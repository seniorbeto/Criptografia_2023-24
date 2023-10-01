from packages.api import ServerAPI
import tracemalloc
import os
import freezegun

tracemalloc.start()
api = ServerAPI()

api.login("user1", "pass1")
print(len(api.get_images(username="@all")))

api.remove_image("2022/01/01", "00_00_00")

print(len(api.get_images(username="@all")))