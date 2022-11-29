
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from src import *


APPLET = 0x80
VERIFY = 0x20
P1_INST_INST = 0x04

INS_RSA_MODULUS = 0x01
INS_RSA_EXPONENT = 0x02
INS_RSA_SIGNATURE = 0x03
pin = [0x00, 0x01, 0x02, 0x03]

cardtype = AnyCardType()
cardrequest = CardRequest(timeout=1, cardType=cardtype)
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()
# observer = ConsoleCardConnectionObserver()
# cardservice.connection.addObserver(observer)

APPLET_AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
APDU_HELLO = [APPLET, 0x00, 0x00, 0x00, 0x00]
APDU_PIN = [APPLET, VERIFY, 0x00, 0x00, 0x04, 0x00, 0x01, 0x02, 0x03]
APDU_SELECT = [0x00, 0xA4, P1_INST_INST, 0x00, len(APPLET_AID)] + APPLET_AID

APDU_RSA_MOD = [APPLET, INS_RSA_MODULUS, 0x00, 0x00, 0x00]
APDU_RSA_EXPONENT = [APPLET, INS_RSA_EXPONENT, 0x00, 0x00, 0x00]
APDU_SIGN = [APPLET, INS_RSA_SIGNATURE, 0x00, 0x00, 0x00]


class SmartCard:
    def __init__(self, connection, debug=False):
        self.connection = connection
        self.PIN = None
        self.debug = debug
        self.verified = False
        self._rsa_key: RSAVerification = None
        self._connect()

    def _connect(self):
        self.cardtype = AnyCardType()
        self.observer = ConsoleCardConnectionObserver()
        if self.debug:
            self.connection.addObserver(self.observer)
        self.PIN = PIN(self.connection, APPLET_AID, APDU_SELECT)

    def verify(self):
        return self.PIN.inputPin()

    def send_apdu(self, apdu):
        response, sw1, sw2 = self.connection.transmit(apdu)
        if sw1 == 0x61 or sw1 == 0x6C:
            response, sw1, sw2 = self.get_response(apdu[1], sw2)
        return response, sw1, sw2

    def select_applet(self):
        return self.send_apdu(APDU_SELECT + [len(APPLET_AID)] + APPLET_AID)

    def hello(self):
        return self.send_apdu(APDU_HELLO)

    def change_pin(self):
        self.PIN.changePin()

    def get_response(self, ins, sw2):
        GET_RESPONSE = [0X80, ins, 0x00, 0x00]
        return self.send_apdu(GET_RESPONSE + [sw2])

    def get_rsa_mod(self):
        return self.send_apdu(APDU_RSA_MOD)

    def get_rsa_exponent(self):
        return self.send_apdu(APDU_RSA_EXPONENT)

    @property
    def rsa_key(self):
        if self._rsa_key is None:
            self._rsa_key = self.ask_rsa_public_key()
        return self._rsa_key

    @rsa_key.setter
    def rsa_key(self):
        self._rsa_key = self.ask_rsa_public_key()

    def ask_rsa_public_key(self):
        response, _, _ = self.get_rsa_mod()
        n = int.from_bytes(bytes(response), byteorder='big')
        response, _, _ = self.get_rsa_exponent()
        e = int.from_bytes(bytes(response), byteorder='big')
        return RSAVerification(n, e)

    def verify_signature(self, message: bytes, signature: bytes):
        return self.rsa_key.verify(message, signature)

    def get_signature(self, message=None):
        return bytes(self.send_apdu(APDU_SIGN)[0])


if __name__ == "__main__":
    card = SmartCard(cardservice.connection, debug=True)
    card.select_applet()
    card.hello()
    card.verify()
    card.hello()
    card.verify_signature(b"Hello", card.get_signature())
    card.change_pin()
