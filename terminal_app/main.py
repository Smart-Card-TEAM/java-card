from smartcard.System import readers
from smartcard.util import toHexString

r=readers()

print(r)

connection = r[0].createConnection()
connection.connect()
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]

data, sw1, sw2 = connection.transmit( SELECT + DF_TELECOM )
print("%x %x" % (sw1, sw2))