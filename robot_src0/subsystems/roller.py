import wpilib
from wpilib.buttons import JoystickButton
from ctre import WPI_TalonSRX
from .led import LEDController

class Roller():

    POSITION_TOP = 1000

    def __init__(self, roller_motor, pivot,stick,initial_state):
        self.roller_motor = roller_motor
        self.pivot = pivot
        self.stick = stick
        self.rollerenabler = JoystickButton(self.stick, 14)
        self.pivotupbutton = JoystickButton(self.stick, 5)
        self.pivotdownbutton = JoystickButton(self.stick, 10)
        #self.pivotstopbutton = JoystickButton(self.stick, 14)
        #self.pivotinitbutton = JoystickButton(self.stick, 13)
        self.rollerout = JoystickButton(self.stick, 6)
        self.rollerin = JoystickButton(self.stick,9)
        self.state = initial_state
        self.pivot.selectProfileSlot(0,0)
        self.switch =  wpilib.DigitalInput(2)

    def update(self):

        if (self.state is not "init") and (not self.rollerenabler.get()):
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.state = "manual"
            return

        if self.state == "manual":
            # if self.pivot.getSelectedSensorPosition() >= self.POSITION_TOP and self.stick.getY() >0:
            #     self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            # else:
            #     self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getY())
            pass

        elif self.pivotupbutton.get():
            #self.pivot.setQuadraturePosition(0)
            self.state = "up"

        elif self.pivotdownbutton.get():
            self.state = "down"

        #elif self.pivotstopbutton.get():
            #self.pivot.setQuadraturePosition(0)
            #self.state = "manual"

        #elif self.pivotinitbutton.get():
        #    self.state = "init"

        self.state_table[self.state](self)

        if self.rollerin.get():
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 1)
        elif self.rollerout.get():
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)
        else:
            self.roller_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)

    def log(self):
        wpilib.SmartDashboard.putString("roller_state", self.state)

    def state_init(self):
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
            self.state = 'manual'

    def state_manual(self):
        pass

    def state_up(self):
        self.pivot.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_TOP)
        if self.pivot.getSelectedSensorPosition() > self.POSITION_TOP + 10:
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.state = 'manual'
    def state_down(self):
        self.pivot.set(
                WPI_TalonSRX.ControlMode.PercentOutput,
                -.4
            )
    state_table = {
        "manual": state_manual,
        "up": state_up,
        "down": state_down,
        "init": state_init
    }
