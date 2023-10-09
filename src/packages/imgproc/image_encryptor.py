from packages.imgproc import *
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image, PngImagePlugin
from .imgproc import *
import os


class ImageEncryptor():
    def __init__(self) -> None:
        pass

    @staticmethod
    def encrypt(img: Image,key: bytes, x, y, widht, height) -> Image:
        """
        Encrypts an image using AES-162 in CBC mode
        :param img: image to be encrypted
        :param password: password to encrypt the image
        :return: encrypted image
        """
        # check if the number of pixels is mupltiple of 8 
        n = (x-widht) * (y-height)
        if n % 8 != 0:
            raise ValueError("The number of pixels must be multiple of 8")
        # check if there are at least 8 pixels
        if n < 8:
            raise ValueError("There must be at least 8 pixels")
        
        # check if key is 192 bits = 24 bytes
        if len(key) != 24:
            raise ValueError("The key must be 192 bits, 24 bytes")


        # randomize iv 16 bytes for cbc in aes 192
        iv = os.urandom(16)
        # write the iv in the image metadata
        ImageEncryptor.__write_iv(img, iv)

        # create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # ENCRYPT
        # get the pixels to encrypt 
        pixels = getColors(img, x, y, widht, height)
        # group them in blocks of 8 pixels
        blocks = []
        for pixel, color in pixels.items():
            print(f"pixel: {pixel}, color: {color}")
            

        # encrypt the pixels
        # TODO
        # separate the pixels from the blocks
        # TODO
        # update the pixels in the image
        # TODO
        # return the encrypted image
        # TODO
        return img



    def __write_iv(img: Image, iv: bytes):
        """
        Writes the iv in the image metadata
        :param img: image
        :param iv: iv to be written
        """
        old_meta_data = img.info
        # print(f"old meta data: {old_meta_data}, type: {type(old_meta_data)}")
        new_meta_data = {"iv": iv.hex()}
        # combine old and new metadata
        new_meta_data.update(old_meta_data)
        # print(f"new meta data: {new_meta_data}, type: {type(new_meta_data)}")
        # write the new metadata
        print(f"write iv: {iv.hex()}")
        img.info = new_meta_data

    def __read_iv(img: Image) -> bytes:
        """
        Reads the iv from the image metadata
        :param img: image
        :return: iv
        """
        meta_data = img.info  # dictioanry
        iv = meta_data["iv"]
        print(f"read iv: {iv}")
        return bytes.fromhex(iv)
