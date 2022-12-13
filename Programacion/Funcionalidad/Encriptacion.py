import base64

from cryptography.fernet import Fernet


class Encriptacion:

    def Encrypt(self, clearText):
        # generate a key for encryption and decryption
        key = b"MAKV2SPBNI99212MAKV2SPBNI9921299"

        # Instance the Fernet class with the key
        fernet = Fernet(base64.urlsafe_b64encode(key))
        encMessage = fernet.encrypt(clearText.encode())

        return encMessage

    def Decrypt(self, cipherText):
        decMessage = "-2"
        try:
            # generate a key for encryption and decryption
            key = b"MAKV2SPBNI99212MAKV2SPBNI9921299"

            # Instance the Fernet class with the key
            fernet = Fernet(base64.urlsafe_b64encode(key))
            decMessage = fernet.decrypt(cipherText).decode()
        except Exception as error:
            print("Error al desencriptar: ", error)
        return decMessage
