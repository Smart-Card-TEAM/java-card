from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA
class RSAVerification:
    def __init__(self, n, e) -> None:
        key_params = (n, e)
        self.key = RSA.construct(key_params)
        print(self.key.exportKey())
        # self.key = self.load_rsa(pub_key)
        # print("Verif: ", self.verify(b"Hello World"))


    def verify(self, message):
        h = SHA.new(b"Hello")
        print(h.hexdigest(), message)
        # signature = pkcs1_15.new(self.key).sign(h)
        verifier = pkcs1_15.new(self.key).verify(h, message)
        if verifier:
            print("The signature is valid.")
        else:
            print("The signature is not valid.")



    # def load_rsa_verify_key_from_hex(self, hex_key):
    #     key = PublicKey.load_pkcs1_openssl_der(
    #         hex_key)
    #     return key
