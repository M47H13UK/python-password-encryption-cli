
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import time
import os
from cryptography.fernet import InvalidToken, Fernet

while True:
    password_provided = input("Password: ")
    if not password_provided:
        print("Password cannot be empty.")
        continue
    password = password_provided.encode()

    mode = input("Encrypt (E) or Decrypt (D): ").strip().upper()
    while mode not in ("E", "D"):
        print("Please enter only 'E' to encrypt or 'D' to decrypt.")
        mode = input("Encrypt (E) or Decrypt (D): ").strip().upper()

    # Generate a random salt if encrypting, or input salt if decrypting
    if mode == "E":
        salt = os.urandom(16)
    else:  # mode == "D"
        while True:
            salt_hex = input("Please provide the salt (in hex format): ").strip()
            try:
                salt = bytes.fromhex(salt_hex)
                break
            except ValueError:
                print("Salt must be a valid hex string (0–9, a–f). Try again.")


    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print('This is the encryption key: ', key)
    print('This is the salt (in hex format): ', salt.hex())

    if mode.upper() == 'E':
        message = input("Message: ").encode()

        f = Fernet(key)
        encrypted1 = f.encrypt(message)
        encrypted_msg = encrypted1.decode()
        print('')
        time.sleep(1)
        print(encrypted_msg)
        print('')
        time.sleep(1)
        print('Would you like to output this message into a text file??')
        choice = input('y/n: ').strip().lower()
        if choice == 'y':
            with open('encrypted_file.txt', 'w', encoding='utf-8') as encrypted_file:
                encrypted_file.write("Message: " + encrypted_msg + "\n\n")
                encrypted_file.write("Salt: " + salt.hex() + "\n")
            os.startfile('encrypted_file.txt')
        print('')
        print('Would you like to exit the program??')
        choice = input('y/n: ').strip().lower()
        if choice == 'y':
            print('Exiting Program...')
            time.sleep(1.5)
            exit()

    elif mode.upper() == 'D':
        encrypted2 = input("The encrypted message: ").encode()
        f = Fernet(key)
        try:
            decrypted = f.decrypt(encrypted2)
            decrypted_msg = decrypted.decode()
            print("Valid Key - Successfully decrypted")
            print('')
            time.sleep(1)
            print('Decrypted message: ', decrypted_msg)
        except InvalidToken as e:
            print('')
            time.sleep(0.5)
            print('X')
            time.sleep(0.5)
            print("Invalid Key - Unsuccessfully decrypted")
            time.sleep(1)
            print('Exiting the Program...')
            time.sleep(1.2)
            exit()

        print('')
        print('Would you like to exit the program??')
        choice = input('y/n: ').strip().lower()
        if choice == 'y':
            print('Exiting Program...')
            time.sleep(1.5)
            exit()

# Credits and inspiration.
# Video : https://www.youtube.com/watch?v=H8t4DJ3Tdrg
# Other Resources: https://nitratine.net/blog/post/encryption-and-decryption-in-python/