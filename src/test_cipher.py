from cryptography.fernet import Fernet

# Generate a random AES key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Data to be encrypted (replace with your own data)
data_to_encrypt = b'This is a secret message.'

# Encrypt the data
encrypted_data = cipher_suite.encrypt(data_to_encrypt)

# Decrypt the data (for demonstration purposes)
decrypted_data = cipher_suite.decrypt(encrypted_data)

# Print the results
print(f"Original Data: {data_to_encrypt}")
print(f"Encrypted Data: {encrypted_data}")
print(f"Decrypted Data: {decrypted_data}")
