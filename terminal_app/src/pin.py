class PINVerification:
    pass

class PIN:
    def __init__(self,connection,AID,APDU_SELECT):
        self.tries_left = 3
        self.AID = AID
        self.APDU_SELECT = APDU_SELECT
        self.CLA = 0x80
        self.INS_AUTH = 0x20
        self.INS_ACTIVATE = 0x01
        self.connection = connection
        print(self.connection)

    def verify(self, pin):
        try:
            pin = [int(x) for x in pin]
        except:
            print("PIN must be numeric")
            return False
        adpu = [self.CLA, self.INS_AUTH, 0x00, 0x00, len(pin)] + pin
        response, sw1 , sw2 = self.connection.transmit(self.APDU_SELECT)
        data, sw1, sw2 = self.connection.transmit(adpu)
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:
            self.tries_left -= 1
            return False

    def inputPin(self):
        verify = False
        while not verify:
            pin = input("Enter PIN: ")
            if len(pin) < 4 or len(pin) > 8:
                print("PIN must be between 4 and 8 digits")
                continue
            verify = self.verify(pin)
            if not verify:
                print("Wrong PIN, %d tries left" % self.tries_left)
            if self.tries_left == 0:
                print ("No more tries left, card blocked")
                return False
        return verify