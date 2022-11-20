from smartcard.System import readers
from smartcard.util import toHexString

r=readers()

print(r)

connection = r[0].createConnection()
connection.connect()
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]

# a00000006203010c060102
aid = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]

data, sw1, sw2 = connection.transmit( SELECT + aid)
print("%x %x" % (sw1, sw2))
print(toHexString([sw1, sw2]))
print(data)