import uuid
from src.system import *
from PIL import Image


def print_metadata(self, image_path):
        image = Image.open(image_path)
        image.load()
        print(image.info)


ser = Server()
ser.delete_all_cameras()
ser.delete_all_users()
ser.create_user("raul", "password 1")
ser.create_user("beto", "password 2")

ser.create_camera("cam1", "raul")
ser.create_camera("cam2", "raul")
ser.create_camera("cam3", "beto")
ser.create_camera("cam4", "beto")

ser.store_image("tests/TEST2.png", "cam1", "raul")

ser.store_image("tests/TEST1.png", "cam2", "raul")

print_metadata(ser, "tests/TEST2.png")
print_metadata(ser, "tests/TEST1.png")

print_metadata(ser, "src/system/data/images/raul/cam2/1694266057.png")