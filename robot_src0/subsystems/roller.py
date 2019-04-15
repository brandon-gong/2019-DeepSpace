import wpilib
from wpilib.buttons import JoystickButton
from ctre import WPI_TalonSRX
from .led import LEDController

class Roller():

    POSITION_TOP = 3100

    def __init__(self, roller_motor, pivot,stick,initial_state):
        self.roller_motor = roller_motor
        self.pivot = pivot
        self.stick = stick
        self.rollerenabler = JoystickButton(self.stick, 14)
        self.pivotupbutton = JoystickButton(self.stick, 5)
        self.pivotdownbutton = JoystickButton(self.stick, 10)
        self.pistonoutbutton = JoystickButton(self.stick, 8)
        self.pistoninbutton = JoystickButton(self.stick, 7)
        #self.ratchetswitchbutton = JoystickButton(self.stick, 15)
        #self.ratchetbtnpressed = False
        #self.pivotstopbutton = JoystickButton(self.stick, 14)
        #self.pivotinitbutton = JoystickButton(self.stick, 13)
        self.rollerout = JoystickButton(self.stick, 9)
        self.rollerin = JoystickButton(self.stick,6)
        self.state = initial_state
        self.pivot.selectProfileSlot(0,0)
        self.switch =  wpilib.DigitalInput(2)
        self.count = 0

        self.sol2 = wpilib.Solenoid(5,3)
        self.sol1 = wpilib.Solenoid(5,0)
        self.sol1.set(False)
        self.sol2.set(True)

        self.ratchet = wpilib.Solenoid(5,6)
        self.ratchetEnabled = False
        self.ratchet.set(not self.ratchetEnabled)
    def update(self):

        if (self.state is not "init") and (not self.rollerenabler.get()):
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.state = "manual"
            self.sol1.set(False)
            self.sol2.set(True)
            return

        if self.state == "manual":
            # if self.pivot.getSelectedSensorPosition() >= self.POSITION_TOP and self.stick.getY() >0:
            #     self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            # else:
            #     self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getY())
            #pass

            if self.pivotupbutton.get():
                #self.pivot.setQuadraturePosition(0)
                self.state = "up"

            elif self.pivotdownbutton.get():
                self.state = "down"

            if self.pistonoutbutton.get():
                self.sol1.set(True)
                self.sol2.set(False)

            if self.pistoninbutton.get():
                self.sol1.set(False)
                self.sol2.set(True)

        #elif self.pivotstopbutton.get():
            #self.pivot.setQuadraturePosition(0)
            #self.state = "manual"

        #elif self.pivotinitbutton.get():
        #    self.state = "init"

        self.state_table[self.state](self)

        if self.rollerin.get():
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)
        #elif self.rollerout.get():
        #    self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)
        else:
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)

    def log(self):
        wpilib.SmartDashboard.putString("roller_state", self.state)
        wpilib.SmartDashboard.putNumber("roller_position", self.pivot.getSelectedSensorPosition())

    def state_init(self):
        self.ratchet.set(not self.ratchetEnabled)
        if self.rollerenabler.get():
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.pivot.setQuadraturePosition(0)
            self.state = 'manual'
            return

        if self.switch.get():
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, -.3)
        else:
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.pivot.setQuadraturePosition(0)
            self.ratchet.set(self.ratchetEnabled)
            self.state = 'manual'

    def state_manual(self):
        pass

    def state_up(self):

        self.pivot.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_TOP)
        #if self.pivot.getSelectedSensorPosition() > self.POSITION_TOP + 500:
        #    self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        #    self.state = 'manual'
        if self.pistonoutbutton.get():
            self.sol1.set(True)
            self.sol2.set(False)

        if self.pistoninbutton.get():
            self.sol1.set(False)
            self.sol2.set(True)

        self.ratchet.set(self.ratchetEnabled)
    def state_down(self):
        self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput,.1)
        self.ratchet.set(not self.ratchetEnabled)

        if self.count == 0:
            self.state = "post_state_down"
        self.count += 1
    def post_state_down(self):
        self.count = 0
        
        self.ratchet.set(not self.ratchetEnabled)

        self.pivot.set(
                WPI_TalonSRX.ControlMode.PercentOutput,
                -.4
            )
        if self.pistonoutbutton.get():
            self.sol1.set(True)
            self.sol2.set(False)

        if self.pistoninbutton.get():
            self.sol1.set(False)
            self.sol2.set(True)



    state_table = {
        "post_state_down": post_state_down,
        "manual": state_manual,
        "up": state_up,
        "down": state_down,
        "init": state_init
    }
