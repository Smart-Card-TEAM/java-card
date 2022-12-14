import logging
import sys


class PIN:
    def __init__(self, connection, AID, APDU_SELECT):
        self.tries_left = 3
        self.AID = AID
        self.APDU_SELECT = APDU_SELECT
        self.CLA = 0x80
        self.INS_AUTH = 0x20
        self.INS_ACTIVATE = 0x04
        self.connection = connection

    def verify(self, pin):
        try:
            pin = [int(x) for x in pin]
        except:
            logging.info("PIN must be numeric")
            return False
        APDU = [self.CLA, self.INS_AUTH, 0x00, 0x00, len(pin)] + pin
        response, sw1, sw2 = self.connection.transmit(self.APDU_SELECT)
        data, sw1, sw2 = self.connection.transmit(APDU)
        if sw1 == 0x67 and sw2 == 0x00:
            logging.info("Card blocked because of too many wrong PINs")
            sys.exit(1)
        elif sw1 == 0x90 and sw2 == 0x00:
            return True
        else:
            self.tries_left -= 1
            return False

    def inputPin(self):
        verify = False
        while not verify:
            pin = input("Enter PIN: ")
            if len(pin) < 4 or len(pin) > 8:
                logging.info("PIN must be between 4 and 8 digits")
                continue
            verify = self.verify(pin)
            if not verify:
                logging.info("Wrong PIN, %d tries left" % self.tries_left)
            if self.tries_left == 0:
                logging.info("No more tries left, card blocked")
                return False
        return verify

    def sendAPDUChangePin(self, new_pin):
        try:
            new_pin = [int(x) for x in new_pin]
        except:
            logging.info("PIN must be numeric")
            return False
        APDU = [self.CLA, self.INS_ACTIVATE,
                0x00, 0x00, len(new_pin)] + new_pin
        data, sw1, sw2 = self.connection.transmit(APDU)
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:
            self.tries_left -= 1
            return False

    def changePin(self):
        changed = False
        while not changed:
            pin = input("Enter new PIN: ")
            if len(pin) < 4 or len(pin) > 8:
                logging.info("PIN must be between 4 and 8 digits")
                continue
            changed = self.sendAPDUChangePin(pin)
            if not changed:
                logging.info("Wrong PIN, %d tries left" % self.tries_left)
            if self.tries_left == 0:
                logging.info("No more tries left, card blocked")
                return False
