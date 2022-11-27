from smartcard.CardConnectionObserver import CardConnectionObserver
from smartcard.util import toHexString, toASCIIString


class ConsoleCardConnectionObserver(CardConnectionObserver):
    def update(self, cardconnection, ccevent):

        if 'connect' == ccevent.type:
            print('connecting to ' + cardconnection.getReader())

        elif 'disconnect' == ccevent.type:
            print('disconnecting from ' + cardconnection.getReader())

        elif 'command' == ccevent.type:
            print('> ', toHexString(ccevent.args[0]))

        elif 'response' == ccevent.type:
            if [] == ccevent.args[0]:
                print('< [] ', "%-2X %-2X" % tuple(ccevent.args[-2:]))
            else:
                print('< ', toASCIIString(
                    ccevent.args[0]), "%-2X %-2X" % tuple(ccevent.args[-2:]))
