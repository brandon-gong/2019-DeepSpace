import wpilib
from wpilib.buttons import JoystickButton
from ctre import WPI_TalonSRX

class MyRobot(wpilib.TimedRobot):

    POSITION_TOP = 3500.0
    POSITION_BOTTOM = 0

    def robotInit(self):
        self.stick = wpilib.Joystick(0)
        self.pivot = WPI_TalonSRX(10)
        self.pull = WPI_TalonSRX(9)
        self.pivotupbutton = JoystickButton(self.stick, 1)
        self.pivotdownbutton = JoystickButton(self.stick, 2)
        self.pivotstopbutton = JoystickButton(self.stick, 3)
        self.pivotinitbutton = JoystickButton(self.stick, 4)
        self.rollerout = JoystickButton(self.stick, 16)
        self.rollerin = JoystickButton(self.stick,11)
        self.pivot.selectProfileSlot(0,0)
        self.state = 'init'
        self.switch =  wpilib.DigitalInput(0)

    # Called repeatedly in a loop while the robot is disabled.
    def disabledPeriodic(self):
        pass
    def state_init(self):
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
        if self.pivot.getSelectedSensorPosition() >= self.POSITION_TOP:
            self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            self.state = 'manual'
    def state_down(self):
        self.pivot.set(
                WPI_TalonSRX.ControlMode.Position,
                self.POSITION_BOTTOM
            )
    state_table = {
        "manual": state_manual,
        "up": state_up,
        "down": state_down,
        "init": state_init
    }
    # Called repeatedly during teleop.
    # Update all of the subsystems and log new data to SmartDashboard.
    def teleopInit(self):
        self.pivot.setQuadraturePosition(0)

    def teleopPeriodic(self):

        if abs(self.stick.getY()) > 0.05:
            self.state = "manual"
            if self.pivot.getSelectedSensorPosition() >= self.POSITION_TOP and self.stick.getY() >0:
                self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
            else:
                self.pivot.set(WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getY())
        elif self.pivotupbutton.get():
            self.pivot.setQuadraturePosition(0)
            self.state = "up"
        elif self.pivotdownbutton.get():
            self.state = "down"
        elif self.pivotstopbutton.get():
            self.pivot.setQuadraturePosition(0)
            self.state = "manual"
        elif self.pivotinitbutton.get():
            self.state = "init"
        self.state_table[self.state](self)
        if self.rollerin.get():
            self.pull.set(WPI_TalonSRX.ControlMode.PercentOutput, 1)
        elif self.rollerout.get():
            self.pull.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)
        else:
            self.pull.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        wpilib.SmartDashboard.putNumber("thingposition", self.pivot.getSelectedSensorPosition())
        print(self.pivot.getSelectedSensorPosition())
if __name__ == "__main__":
    wpilib.run(MyRobot)
