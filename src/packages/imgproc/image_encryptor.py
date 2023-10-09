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
        n = (x-widht) * (y-height)
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
        iv = os.urandom(16)
        # write the iv in the image metadata
        ImageEncryptor.__write_iv(img, iv)

        # create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # ENCRYPT
        # get the pixels to encrypt 
        pixels = getColors(img, x, y, widht, height)
        # group them in blocks of 
        blocks = [] # list of blocks, each block is 48 bytes = 16 pixels
        current_block = b''
        i = 0
        for pixel, color in pixels.items():
            if i == 16:
                blocks.append(current_block)
                current_block = b''
                i = 0
            current_block += bytes.fromhex(color)
            i += 1
        
        # encrypt the blocks
        encrypted_blocks = []
        for block in blocks:
            encrypted_blocks.append(encryptor.update(block).hex())
            # print(f"block: {block.hex()}")

        # separate the encrypted blocks in pixels, each block is 48 bytes = 16 pixels
        pixels_keys = list(pixels.keys())
        new_pixels = {}
        for i in range(len(encrypted_blocks)):
            block = encrypted_blocks[i]
            for j in range(16-1):
                # print(f"pixel key: {pixels_keys[i*16 + j]}", end=". ")
                new_pixels[pixels_keys[i*16 + j]] = block[6*j:6*j+6]
            print()
        # print(f"old pixels len: {len(pixels)}")
        # print(f"nº  of  blocks: {len(blocks)}")
        # print(f"nº of old pixels: {len(blocks)*16}")
        # print()
        # print(f"nº of encrypted blocks: {len(encrypted_blocks)}")
        # print(f"nº of new pixels: {len(encrypted_blocks)*16}")
        # print(f"new pixels len: {len(new_pixels)}")

        # update the pixels in the image
        updatePixelsFromDict(img, x, y, widht, height, pixels)

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
