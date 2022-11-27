
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardConnectionObserver import CardConnectionObserver
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
# r=readers()


class ConsoleCardConnectionObserver( CardConnectionObserver ):
    def update( self, cardconnection, ccevent ):

        if 'connect'==ccevent.type:
            print('connecting to ' + cardconnection.getReader())

        elif 'disconnect'==ccevent.type:
            print('disconnecting from ' + cardconnection.getReader())

        elif 'command'==ccevent.type:
            print ('> ', toHexString( ccevent.args[0] ))

        elif 'response'==ccevent.type:
            if []==ccevent.args[0]:
                print ('< [] ', "%-2X %-2X" % tuple(ccevent.args[-2:]))
            else:
                print('< ', toHexString(ccevent.args[0]), "%-2X %-2X" % tuple(ccevent.args[-2:]))


# print(r)
applet = 0x80
Verfiy = 0x20
# connection = r[0].createConnection()
# connection.connect()


DF_TELECOM = [0x7F, 0x10]


AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
print(len(AID))
pin = [0x00, 0x01, 0x02, 0x03]
SELECT = [0x00, 0xC0, 0x0, 0x0, len(pin)]

APDU = [applet, Verfiy, 0x00, 0x00, 0x04, 0x00, 0x01, 0x02, 0x03]

APDUTEST =  [0x00, 0xA4, 0x04, 0x0c, 0x0B, 0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
# data, sw1, sw2 = connection.transmit( SELECT + AID + APDU )
# print("%x %x %s" % (sw1, sw2, data))

# print(APDU)
# data , sw1 , sw2 = connection.transmit(SELECT + APDU)
# print("%x %x %s" % (sw1, sw2, data))

apduHello = [0x80, 0x00, 0x00, 0x00, 0x00]
SELECT = [0x00, 0xC0, 0x0, 0x0, len(apduHello)]

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=1, cardType=cardtype )
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()
observer=ConsoleCardConnectionObserver()
cardservice.connection.addObserver(observer)
# apdu = SELECT+DF_TELECOM
# print("Sending: %s" % toHexString(SELECT + DF_TELECOM))
# response, sw1, sw2 = cardservice.connection.transmit(SELECT + DF_TELECOM, CardConnection.T0_protocol )
# print("%x %x %s" % (sw1, sw2, response))


print("Sending: %s" % toHexString(SELECT + apduHello))
response, sw1, sw2 = cardservice.connection.transmit(SELECT + apduHello)
print("%x %x %s" % (sw1, sw2, response))
GET_RESPONSE = [0XA0, 0XC0, 00, 00]
apdu = GET_RESPONSE + [sw2]
response, sw1, sw2 = cardservice.connection.transmit(apdu, CardConnection.T0_protocol )
print("%x %x %s" % (sw1, sw2, response))
# from smartcard.System import readers
# from smartcard.util import toHexString

# r=readers()

# print(f"reader {r} detected")

# applet = 0x80
# Verfiy = 0x20
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
# DF_TELECOM = [0x7F, 0x10]
# try :
#     connection = r[0].createConnection()
#     connection.connect()
#     data , sw1 , sw2 = connection.transmit(SELECT + DF_TELECOM)
#     print(f"sw1: {sw1} sw2: {sw2} data: {data}")
# except:
#     print("No reader detected")

# def to_hex(data):
#     return [int(x) for x in data]

# def verify():
#     valid = False
#     while not valid :
#         pin = input("Enter PIN: ")
#         print(to_hex(pin))
#         if len(pin) != 4:
#             print("Invalid PIN length")
#             continue
#         else:
#             APDU = [applet, Verfiy, 0x00, 0x00, 0x04, 0x00, 0x01, 0x02, 0x03]
#             print(APDU)
#             data , sw1 , sw2 = connection.transmit(APDU)
#             print(f"sw1: {sw1} sw2: {sw2} data: {data}")
#             if sw1 == 0x90 and sw2 == 0x00:
#                 print("Valid PIN")
#                 valid = True
#             else:
#                 print("Invalid PIN")
#                 continue




# if __name__ == "__main__":
#     verify()



# """"
# connection = r[0].createConnection()
# connection.connect()
# SELECT =  [0x00, 0xA4, 0x04, 0x00, 0x0A, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00]

# DF_TELECOM = [0x7F, 0x10]

# # a00000006203010c060102
# aid = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]

# data, sw1, sw2 = connection.transmit( SELECT)
# print("%x %x" % (sw1, sw2))
# print(toHexString([sw1, sw2]))
# print(data)"""
