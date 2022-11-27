class PINVerification:
    pass

class PIN:
    def __init__(self,connection,AID):
        self.tries_left = 3
        self.AID = AID
        self.CLA = 0x80
        self.INS_AUTH = 0x20
        self.INS_ACTIVATE = 0x01
        self.connection = connection

    def verify(self, pin):
        adpu = [self.CLA, self.INS_AUTH, 0x00, 0x00, len(pin)] + pin
        data, sw1, sw2 = self.connection.transmit(adpu)
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:
            self.tries_left -= 1
            return False