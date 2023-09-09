"""
This module contains functions for image processing.
"""

from PIL import Image
from random import randint as rd
import pprint as pp

def rgbToHex(rgb: tuple) -> str:
    """
    Converts a tuple of RGB values to a hexadecimal color code.
    """
    if len(rgb) != 3:
        raise ValueError("The tuple must contain 3 values.")
    for i in rgb:
        if i < 0 or i > 255:
            raise ValueError("The rgb values must be between 0 and 255.")

    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])

def hexToRgb(hex: str | int) -> tuple:
    """
    Converts a hexadecimal color code to a tuple of RGB values.
    """
    if type(hex) == int and hex < 0 or hex > 0xFFFFFF:
        raise ValueError("The hex value must be between 0 and 0xFFFFFF.")
    elif type(hex) == str and len(hex) != 7 and hex[0] != "#":
        raise ValueError("The hex value must be a string of length 7.")

    if type(hex) == str and hex[0] == "#":
        return (int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16))
    else:
        return (int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))

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
                color_hex = rgbToHex(color)
                colors[(j, i)] = color_hex
    else:
        for i in range(y, height + y):
            for j in range(x, width + x):
                color = image.getpixel((i, j))
                color_hex = rgbToHex(color)
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
    for _ in range(5):
        for _ in range(5):
            new.append((255, 0, 0))

    updatePixels("data/shrek.jpg", 0, 0, 5, 5, new)
    pp.pprint(getColors("new_image.jpg", 0, 0, 5, 5))

