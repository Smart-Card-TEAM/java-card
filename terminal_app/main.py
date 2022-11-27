
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from src import *



APPLET = 0x80
VERIFY = 0x20
INS_DELETE = 0xE4
INS_INSTALL = 0xE6
INS_LOAD = 0xE8
P1_INST_LOAD = 0x02
P1_INST_INST = 0x04
P1_INST_MSEL = 0x08
P1_INST_INSMSEL = P1_INST_INST | P1_INST_MSEL
P1_INST_EXTRA = 0x10
P1_INST_PERSO = 0x20
P1_INST_REGUPD = 0x40

pin = [0x00, 0x01, 0x02, 0x03]

cardtype = AnyCardType()
cardrequest = CardRequest(timeout=1, cardType=cardtype)
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()
observer = ConsoleCardConnectionObserver()
cardservice.connection.addObserver(observer)

APPLET_AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
APDU_PIN = [APPLET, VERIFY, 0x00, 0x00, 0x04, 0x00, 0x01, 0x02, 0x03]
APDU_SELECT = [0x00, 0xA4, 0x04, 0x00, len(APPLET_AID)] + APPLET_AID
APDU_HELLO = [APPLET, 0x00, 0x00, 0x00, 0x05]

APDU_RSA_EXPONENT = [APPLET, 0x01, 0x00, 0x00, 0x05]

response, sw1, sw2 = cardservice.connection.transmit(APDU_SELECT)
response, sw1, sw2 = cardservice.connection.transmit(APDU_PIN)
response, sw1, sw2 = cardservice.connection.transmit(APDU_HELLO)


response, sw1, sw2 = cardservice.connection.transmit(APDU_RSA_EXPONENT)
class SmartCard:
    pass


# if __name__ == "__main__":
#     card = SmartCard()