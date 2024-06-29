from app import app

from cryptography.fernet import Fernet


class PasswordSecure:
    # This SECRET_KEY should ideally be securely stored and not hard-coded in a production environment
    key = app.config['SECRET_KEY']

    cipher_suite = Fernet(key)

    @staticmethod
    def encryption(plaintext):
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext = PasswordSecure.cipher_suite.encrypt(plaintext_bytes)
        return ciphertext.decode('utf-8')

    @staticmethod
    def decryption(ciphertext):
        ciphertext_bytes = ciphertext.encode('utf-8')
        plaintext = PasswordSecure.cipher_suite.decrypt(ciphertext_bytes)
        return plaintext.decode('utf-8')



