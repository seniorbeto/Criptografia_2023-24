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
    def decrypt(img: Image, password:str, x, y, width, height) -> Image:
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
        if x + width >= img.width or y + height >= img.height:
            x = 0
            y = 0
            width = (img.width // 16) * 16
            height = (img.height // 16) * 16
            # print("WARNING: The specified region is out of bounds. The whole image will be decrypted")
            # print(f"new x: {x}, new y: {y}, new width: {width}, new height: {height}")
            # print(f"img width: {img.width}, img height: {img.height}")
            # print(f"new widht%16 = {width % 16}, new height%16 = {height % 16}")

        # get the iv from the image metadata
        iv, salt = ImageEncryptor.__read_salt_and_iv(img)

        # generate key from password
        key = PBKDF2HMAC(
            salt=salt,
            length=24,  # 24 bytes = 192 bits
            algorithm=hashes.SHA256(),
            iterations=100000
        ).derive(password.encode())

        print(f"DECRYPTOR key: {key.hex()}, password: {password}, salt: {salt.hex()}")

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
    def encrypt(img: Image, password: str, x, y, widht, height) -> Image:
        """
        Encrypts an image using AES-192 in CBC mode
        :param img: image to be encrypted
        :param password: password  for the PBKDF to generate the key
        :return: encrypted image
        """
        # comprobar que x+w < width y y+h < height
        if x + widht >= img.width or y + height >= img.height:
            x = 0
            y = 0
            widht = (img.width // 16) * 16
            height = (img.height // 16) * 16
            # print("WARNING: The specified region is out of bounds. The whole image will be encrypted")
            # print(f"new x: {x}, new y: {y}, new width: {widht}, new height: {height}")
            # print(f"img width: {img.width}, img height: {img.height}")
            # print(f"new widht%16 = {widht % 16}, new height%16 = {height % 16}")

        # cada pixel son 6hex = 3 bytes, necesito bloques de tamaño multiplo de 16 bytes (tamaño de bloque de aes)
        # necesito bloques de 48 bytes = 16 pixeles 
        # check if the number of pixels is mupltiple of 16 
        n = (widht) * (height) # number of pixels
        if n % 16 != 0:
            print(f"x: {x}, y: {y}, width: {widht}, height: {height}, n: {n}")
            raise ValueError("The number of pixels must be multiple of 16")
        # check if there are at least 16 pixels
        if n < 16:
            raise ValueError("There must be at least 16 pixels")
        # generate key from password 
        # generate salt
        salt = os.urandom(16)
        key = PBKDF2HMAC(
            salt = salt,
            length = 24, # 24 bytes = 192 bits
            algorithm=hashes.SHA256(),
            iterations=100000
        ).derive(password.encode())
        print(f"ENCRYPTOR key: {key.hex()}, password: {password}, salt: {salt.hex()}")
        # check if key is 192 bits = 24 bytes #FIXME REMOVE
        if len(key) != 24:
            raise ValueError("The key must be 192 bits, 24 bytes")


        # randomize iv 16 bytes for cbc in aes 192
        iv = os.urandom(16)
        # write the iv and salt in the image metadata
        ImageEncryptor.__write_salt_and_iv(img, iv, salt)

        # create cipher
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        encryptor = cipher.encryptor()
        
        # ENCRYPT
        # get the pixels to encrypt 
        pixels = getColors(img, x, y, widht, height)
        new_pixels = {}
        for pixel, color in pixels.items():
            block = bytearray()
            block += encryptor.update(color) # color es un bytearray de 3 bytes
            new_pixels[pixel] = block

        updatePixelsFromDict(img, x, y, widht, height, new_pixels)

        return img



    def __write_salt_and_iv(img: Image, iv: bytes, salt: bytes):
        """
        Writes the iv in the image metadata
        :param img: image
        :param iv: iv to be written
        """
        old_meta_data = img.info
        # print(f"old meta data: {old_meta_data}, type: {type(old_meta_data)}")
        new_meta_data = {"iv": iv.hex(), "salt": salt.hex(), "algo": "AES-192"}

        # combine old and new metadata
        new_meta_data.update(old_meta_data)
        # print(f"new meta data: {new_meta_data}, type: {type(new_meta_data)}")
        # write the new metadata
        img.info = new_meta_data

    def __read_salt_and_iv(img: Image) -> (bytes, bytes):
        """
        Reads the iv from the image metadata
        :param img: image
        :return: (iv, salt)
        """
        meta_data = img.info  # dictioanry
        iv = bytes.fromhex(meta_data["iv"])
        salt = bytes.fromhex(meta_data["salt"])

        return (iv, salt)
