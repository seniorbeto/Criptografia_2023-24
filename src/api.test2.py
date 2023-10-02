from packages.api import ServerAPI
import tracemalloc
import os
import freezegun
from PIL import Image

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


test = hashes.Hash(hashes.SHA256())
test.update("test".encode())
test = test.finalize()
print(test)

bytes.fromhex(test.hex())

print(bytes.fromhex(test.hex()))