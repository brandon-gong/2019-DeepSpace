import wpilib

class LEDController():

    STATE_DISABLED = 0
    STATE_RED_MOTION = 1
    STATE_BLUE_MOTION = 2
    STATE_LIFT_UP = 3
    STATE_LIFT_DOWN = 4
    STATE_BALL_MOTION = 5
    STATE_RED_STANDBY = 6
    STATE_GAME_OVER = 7
    STATE_BLUE_STANDBY = 8
    STATE_STOP_LIFT =9
    STATE_HATCH = 10
    STATE_SHOE_1 = 11


    __instance = None

    class __LEDController():
        def __init__(self):
            try:
                self.serial = wpilib.SerialPort(9600,2)
                #self.serial.writeString("5002")
            except:
                print("Couldn't Open Port")
            self.state = 0
            self.last = self.state

        def update(self):
            if self.state == self.last:
                pass
            else:
                try:
                    self.serial.writeString(str(self.state))
                    self.last = self.state
                except:
                    print("Write to serial port failed.")
                    pass

        def log(self):
            wpilib.SmartDashboard.putNumber("ledstate", self.state)

        def setState(self, newstate):
            self.state = newstate

        def getState(self):
            return self.state

    def __init__(self):
        if not LEDController.__instance:
            LEDController.__instance = LEDController.__LEDController()

    def getInstance():
        return LEDController.__instance
