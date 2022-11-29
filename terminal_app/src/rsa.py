from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA


class RSAVerification:
    def __init__(self, n, e) -> None:
        key_params = (n, e)
        self.key = RSA.construct(key_params)
        print(self.key.export_key())

    def verify(self, message: bytes, signature: bytes):
        h = SHA.new(message)
        try:
            pkcs1_15.new(self.key).verify(h, signature)
            print("The signature is valid.")
            return True
        except:
            print("The signature is not valid.")
            return False
