from packages.imgproc import *
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image, PngImagePlugin
from .imgproc import *
import os


class ImageEncryptor():
    def __init__(self) -> None:
        pass

    @staticmethod
    def decrypt(img: Image, password:str) -> Image:
        """
        Decrypts an image using AES-192 in CBC mode
        :param img: the image to be decrypted
        :param key: the key to decrypt the image
        :param x:
        :param y:
        :param width:
        :param height:
        :return: decrypted image
        """

        # get the iv from the image metadata
        metadata = ImageEncryptor.__read_metadata(img)
        iv = bytes.fromhex(metadata["iv"])
        salt = bytes.fromhex(metadata["salt"])
        x = int(metadata["x"])
        y = int(metadata["y"])
        width = int(metadata["width"])
        height = int(metadata["height"])

        # generate key from password
        key = PBKDF2HMAC(
            salt=salt,
            length=24,  # 24 bytes = 192 bits
            algorithm=hashes.SHA256(),
            iterations=100000
        ).derive(password.encode())

        # print(f"DECRYPTOR key: {key.hex()}, password: {password}, salt: {salt.hex()}")

        # create cipher
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        decryptor = cipher.decryptor()

        # DECRYPT
        # get the pixels to decrypt
        pixels = getColors(img, x, y, width, height)
        new_pixels = {}
        for pixel, color in pixels.items():
            block = bytearray()
            block += decryptor.update(color)
            new_pixels[pixel] = block

        updatePixelsFromDict(img, x, y, width, height, new_pixels)

        return img

    @staticmethod
    def encrypt(img: Image, password: str, x, y, width, height) -> Image:
        """
        Encrypts an image using AES-192 in CBC mode
        :param img: image to be encrypted
        :param password: password  for the PBKDF to generate the key
        :return: encrypted image
        """
        # cada pixel son 6hex = 3 bytes, necesito bloques de tamaño multiplo de 16 bytes (tamaño de bloque de aes)
        # necesito bloques de 48 bytes = 16 pixeles 
        # check if the number of pixels is mupltiple of 16 
        # generate key from password 
        # generate salt
        salt = os.urandom(16)
        key = PBKDF2HMAC(
            salt = salt,
            length = 24, # 24 bytes = 192 bits
            algorithm=hashes.SHA256(),
            iterations=100000
        ).derive(password.encode())
        #  print(f"ENCRYPTOR key: {key.hex()}, password: {password}, salt: {salt.hex()}")
        # check if key is 192 bits = 24 bytes #FIXME REMOVE
        if len(key) != 24:
            raise ValueError("The key must be 192 bits, 24 bytes")


        # randomize iv 16 bytes for cbc in aes 192
        iv = os.urandom(16)
        # write the iv and salt in the image metadata
        
        metadata = {"iv": iv.hex(), 
                    "salt": salt.hex(), 
                    "algo": "AES-192",
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    }
        ImageEncryptor.__write_metadata(img, metadata)

        # create cipher
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        encryptor = cipher.encryptor()
        
        # ENCRYPT
        # get the pixels to encrypt 
        pixels = getColors(img, x, y, width, height)
        new_pixels = {}
        for pixel, color in pixels.items():
            block = bytearray()
            block += encryptor.update(color) # color es un bytearray de 3 bytes
            new_pixels[pixel] = block

        updatePixelsFromDict(img, x, y, width, height, new_pixels)

        return img


    @staticmethod
    def __write_metadata(img: Image, new_metadata: dict) -> None:
        """
        Writes the iv in the image metadata
        :param img: image
        :param iv: iv to be written
        """
        old_meta_data = img.info
        # print(f"old meta data: {old_meta_data}, type: {type(old_meta_data)}")
        # combine old and new metadata
        old_meta_data.update(new_metadata)
        # print(f"new meta data: {new_meta_data}, type: {type(new_meta_data)}")
        # write the new metadata
        img.info = old_meta_data
    
    @staticmethod
    def __read_metadata(img: Image) -> dict:
        """
        Reads the iv from the image metadata
        :param img: image
        :return: (iv, salt)
        """
        return img.info
