"""
This module contains functions for image processing.
"""

from PIL import Image
from random import randint as rd
import pprint as pp

def getColors(file: str, x: int = None, y: int = None, width: int = None, height: int = None) -> dict:
    """
    Returns a dictionary where the keys are the coordinates of the pixels and the values are the colors of each pixel
    in hexadecimal format of a specified region of an image. If no region is specified, the colors of the whole image
    will be returned.
    """
    image = Image.open(file)
    colors = {}

    if not x and not y and not width and not height:
        # If not size is specified, return the colors of the whole image
        width, height = image.size
        for i in range(height):
            for j in range(width):
                color = image.getpixel((j, i))
                color_hex = "#{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])
                colors[(j, i)] = color_hex
    else:
        for i in range(y, height + y):
            for j in range(x, width + x):
                color = image.getpixel((i, j))
                color_hex = "#{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])
                colors[(i, j)] = color_hex
    image.close()

    return colors

def updatePixels(file: str, x: int, y: int, width: int, height: int, color: tuple | list) -> None:
    """
    Updates the pixels of an image given the coordinates of the top left corner, the width and height of the rectangle.
    The color argument can be either a tuple or a dictionary. If it is a tuple, then all the pixels in the specified
    region will be painted with the same color. If it is a list, it's length must be equal to the number of pixels in
    the specified region. The pixels will be painted with the colors in the list in the order they appear in it.
    """
    # Check if the color is a tuple or a dictionary
    if type(color) == list and len(color) != width * height:
        raise ValueError("The number of colors must be equal to the number of pixels in the specified region.")

    image = Image.open(file)

    # If the color argument is a tuple
    if type(color) == tuple:
        for i in range(y, height + y):
            for j in range(x, width + x):
                image.putpixel((i, j), color)

    # If the color argument is a list
    elif type(color) == list:
        for i in range(y, height + y):
            for j in range(x, width + x):
                image.putpixel((i, j), color[i * j])

    image.save("new_image.jpg")
    image.close()


if __name__ == '__main__':

    new = []
    for _ in range(50):
        for _ in range(100):
            new.append((rd(0, 255), rd(0, 255), rd(0, 255)))

    updatePixels("data/shrek.jpg", 0, 0, 50, 100, new)

