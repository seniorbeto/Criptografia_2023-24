from src.packages.system import *
from PIL import Image


if __name__ == '__main__':
    test = Server()
    images = test.get_camera_images(16)