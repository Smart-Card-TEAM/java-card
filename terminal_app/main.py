
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from src import *
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s - %(levelname)s] - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

APPLET = 0x80
VERIFY = 0x20
P1_INST_INST = 0x04

INS_RSA_MODULUS = 0x01
INS_RSA_EXPONENT = 0x02
INS_RSA_SIGNATURE = 0x03
INS_REGISTER_MESSAGE = 0x06
INS_SEND_REGISTERED_MESSAGE = 0x07

APPLET_AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
APDU_HELLO = [APPLET, 0x00, 0x00, 0x00, 0x00]
APDU_PIN = [APPLET, VERIFY, 0x00, 0x00, 0x04, 0x00, 0x01, 0x02, 0x03]
APDU_SELECT = [0x00, 0xA4, P1_INST_INST, 0x00, len(APPLET_AID)] + APPLET_AID

APDU_RSA_MOD = [APPLET, INS_RSA_MODULUS, 0x00, 0x00, 0x00]
APDU_RSA_EXPONENT = [APPLET, INS_RSA_EXPONENT, 0x00, 0x00, 0x00]
APDU_SIGN = [APPLET, INS_RSA_SIGNATURE, 0x00, 0x00, 0x00]
APDU_REGISTER = [APPLET, INS_REGISTER_MESSAGE, 0x00, 0x00]
APDU_SEND_REGISTERED = [APPLET, INS_SEND_REGISTERED_MESSAGE, 0x00, 0x00, 0x00]


def start():
    print("""   ___  ___  _   _  ___  _____   ___  ____________   _____  _____  _____  _____
  |_  |/ _ \| | | |/ _ \/  __ \ / _ \ | ___ \  _  \ / __  \|  _  ||  _  ||  _  |
    | / /_\ \ | | / /_\ \ /  \// /_\ \| |_/ / | | | `' / /'| |/' || |/' || |/' |
    | |  _  | | | |  _  | |    |  _  ||    /| | | |   / /  |  /| ||  /| ||  /| |
/\__/ / | | \ \_/ / | | | \__/\| | | || |\ \| |/ /  ./ /___\ |_/ /\ |_/ /\ |_/ /
\____/\_| |_/\___/\_| |_/\____/\_| |_/\_| \_|___/   \_____/ \___/  \___/  \___/

                                                                                """)


class SmartCard:
    def __init__(self, connection, debug=False):
        self.connection = connection
        self.PIN = None
        self.debug = debug
        self.verified = False
        self._rsa_key: RSAVerification = None
        self.last_signed_message = None
        self._connect()

    def _connect(self):
        logging.info(f"Connected to card {cardservice.connection.getReader()}")

        if self.debug:
            self.connection.addObserver(ConsoleCardConnectionObserver())
        self.PIN = PIN(self.connection, APPLET_AID, APDU_SELECT)

    def verify(self):
        return self.PIN.inputPin()

    def send_apdu(self, apdu):
        response, sw1, sw2 = self.connection.transmit(apdu)
        if sw1 == 0x61 or sw1 == 0x6C:
            response, sw1, sw2 = self.get_response(apdu[1], sw2)
        return response, sw1, sw2

    def select_applet(self):
        logging.info(f"Selecting applet...")
        return self.send_apdu(APDU_SELECT + [len(APPLET_AID)] + APPLET_AID)

    def hello(self):
        return self.send_apdu(APDU_HELLO)

    def change_pin(self):
        self.PIN.changePin()

    def get_response(self, ins, sw2):
        GET_RESPONSE = [0X80, ins, 0x00, 0x00]
        return self.connection.transmit(GET_RESPONSE + [sw2])

    def get_n(self):
        return self.rsa_key.key.n

    def get_e(self):
        return self.rsa_key.key.e

    def get_rsa_mod(self):
        response, _, _ = self.send_apdu(APDU_RSA_MOD)
        return response

    def get_rsa_exponent(self):
        response, _, _ = self.send_apdu(APDU_RSA_EXPONENT)
        return response

    @property
    def rsa_key(self):
        if self._rsa_key is None:
            logging.info(
                "No public key loaded, asking for RSA public key to SmartCard...")
            self._rsa_key = self.ask_rsa_public_key()
        return self._rsa_key

    @rsa_key.setter
    def rsa_key(self):
        self._rsa_key = self.ask_rsa_public_key()

    def ask_rsa_public_key(self):
        response = self.get_rsa_mod()
        n = int.from_bytes(bytes(response), byteorder='big')
        response = self.get_rsa_exponent()
        e = int.from_bytes(bytes(response), byteorder='big')
        return RSAVerification(n, e)

    def verify_signature(self, message: bytes):
        if self.last_signed_message is None:
            logging.info("No message signed")
            return False
        return self.rsa_key.verify(message, self.last_signed_message)

    def register_message(self, message=None):
        if len(message) >= 128:
            logging.error(f"Message too long max length is 127. Please retry.")
            raise ValueError("Message too long")
        m_bytes = [int(x) for x in message.encode("utf-8")]
        apdu = (APDU_REGISTER + [len(m_bytes)] + m_bytes)
        response, _, _ = self.connection.transmit(apdu)
        return response

    def sign_message_registered(self, message=None):
        try:
            self.register_message(message)
        except ValueError:
            return
        self.last_signed_message = bytes(
            self.send_apdu(APDU_SEND_REGISTERED)[0])
        logging.info(
            f"Signature from SmartCard: {self.last_signed_message.hex()}")
        return self.last_signed_message

    def interactive_shell(self) -> None:
        self.select_applet()
        self.verify()
        while True:
            print("1 - Change PIN")
            print("2 - Get RSA modulus")
            print("3 - Get RSA exponent")
            print("4 - Get RSA public key")
            print("5 - Verify signature {}".format("(Last signature: " + self.last_signed_message.hex() +
                  ")" if self.last_signed_message is not None else "(No message have been signed yet)"))
            print("6 - Sign message")
            print("0 - Exit")
            choice = input("Your choice : \n>> ")
            if choice == "1":
                self.change_pin()
                self.verify()
            elif choice == "2":
                logging.info(f"n : {self.get_n()}")
            elif choice == "3":
                logging.info(f"e: {self.get_e()}")
            elif choice == "4":
                print(self.rsa_key.key.export_key().decode("utf-8"))
            elif choice == "5":
                message = input("Message to verify: ")
                logging.info(f"Checking \"{message}\" signature")
                self.verify_signature(message.encode("utf-8"))
            elif choice == "6":
                message = input("Message to sign: ")
                self.sign_message_registered(message)

            elif choice == "0":
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    start()
    cardtype = AnyCardType()
    cardrequest = CardRequest(timeout=None, cardType=cardtype)
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect()
    card = SmartCard(cardservice.connection)
    card.interactive_shell()
    cardservice.connection.disconnect()
