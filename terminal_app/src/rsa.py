from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA
import logging

class RSAVerification:
    def __init__(self, n, e) -> None:
        key_params = (n, e)
        self.key = RSA.construct(key_params)

    def verify(self, message: bytes, signature: bytes):
        h = SHA.new(message)
        try:
            pkcs1_15.new(self.key).verify(h, signature)
            logging.info("The signature is valid.")
            return True
        except:
            logging.info("The signature is not valid.")
            return False
