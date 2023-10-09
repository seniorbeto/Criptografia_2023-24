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
        Encrypts an image using AES-192 in CBC mode
        :param img: image to be encrypted
        :param password: password to encrypt the image
        :return: encrypted image
        """
        # comprobar que x+w < width y y+h < height
        if x + widht >= img.width or y + height >= img.height:
            x = 0
            y = 0
            widht = (img.width // 16) * 16
            height = (img.height // 16) * 16
            print("WARNING: The specified region is out of bounds. The whole image will be encrypted")
            print(f"new x: {x}, new y: {y}, new width: {widht}, new height: {height}")
            print(f"img width: {img.width}, img height: {img.height}")
            print(f"new widht%16 = {widht % 16}, new height%16 = {height % 16}")

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
        
        # check if key is 192 bits = 24 bytes
        if len(key) != 24:
            raise ValueError("The key must be 192 bits, 24 bytes")


        # randomize iv 16 bytes for cbc in aes 192
        nonce = os.urandom(16)
        # write the nonce in the image metadata
        ImageEncryptor.__write_nonce(img, nonce)

        # create cipher
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        
        # ENCRYPT
        # get the pixels to encrypt 
        pixels = getColors(img, x, y, widht, height)
        # group them in blocks of 
        block = bytearray() 
        for pixel, color in pixels.items():
            block += color # color es un bytearray de 3 bytes

        encripted_block = encryptor.update(block)

        
        # separate the encrypted blocks in pixels, each block is 48 bytes = 16 pixels
        pixels_keys = list(pixels.keys())
        print(f"len encripted_block //3: {len(encripted_block)//3}")
        print(f"len pixels_keys: {len(pixels_keys)}")

        new_pixels = {}
        iteraciones = 0
        for i in range(widht-1):
            for j in range(height-1):
                new_pixels[(i, j)] = encripted_block[0:3]
                # print(f"new pixel: {new_pixels[(i, j)]}")
                encripted_block = encripted_block[3:]
                iteraciones += 1
        print(f"iteraciones: {iteraciones}")


        
            # print()
        # print(f"old pixels len: {len(pixels)}")
        # print(f"nº  of  blocks: {len(blocks)}")
        # print(f"nº of old pixels: {len(blocks)*16}")
        # print()
        # print(f"nº of encrypted blocks: {len(encrypted_blocks)}")
        # print(f"nº of new pixels: {len(encrypted_blocks)*16}")
        # print(f"new pixels len: {len(new_pixels)}")

        # update the pixels in the image
        updatePixelsFromDict(img, x, y, widht, height, new_pixels)

        return img



    def __write_nonce(img: Image, nonce: bytes):
        """
        Writes the nonce in the image metadata
        :param img: image
        :param nonce: nonce to be written
        """
        old_meta_data = img.info
        # print(f"old meta data: {old_meta_data}, type: {type(old_meta_data)}")
        new_meta_data = {"nonce": nonce.hex()}
        # combine old and new metadata
        new_meta_data.update(old_meta_data)
        # print(f"new meta data: {new_meta_data}, type: {type(new_meta_data)}")
        # write the new metadata
        print(f"write nonce: {nonce.hex()}")
        img.info = new_meta_data

    def __read_nonce(img: Image) -> bytes:
        """
        Reads the nonce from the image metadata
        :param img: image
        :return: nonce
        """
        meta_data = img.info  # dictioanry
        nonce = meta_data["nonce"]
        print(f"read nonce: {nonce}")
        return bytes.fromhex(nonce)
