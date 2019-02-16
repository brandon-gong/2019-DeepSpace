from ctre import WPI_TalonSRX
from wpilib.buttons import JoystickButton
import wpilib

class Lift():

    POSITION_MAX          = -6.624 * (10**4)
    POSITION_HATCH_TOP    = -6.600 * (10**4)
    POSITION_HATCH_MIDDLE = -3.547 * (10**4)
    POSITION_HATCH_BOTTOM =  0.000

    POSITION_BALL_TOP     = -6.324 * (10**4)
    POSITION_BALL_MIDDLE  = -5.670 * (10**4)
    POSITION_BALL_BOTTOM  = -2.632 * (10**4)

    POSITION_HUMAN_PLAYER = -3.993 * (10**4)

    def __init__(self,liftTalon,stick):
        self.lift_motor = liftTalon

        self.manual_up    = JoystickButton(stick, 4)
        self.manual_down  = JoystickButton(stick, 3)
        self.ball_bottom  = JoystickButton(stick, 5)
        self.ball_middle  = JoystickButton(stick, 6)
        self.ball_top     = JoystickButton(stick, 7)
        self.hatch_bottom = JoystickButton(stick, 10)
        self.hatch_middle = JoystickButton(stick, 9)
        self.hatch_top    = JoystickButton(stick, 8)

        self.state = "manual_stop"

    def getTalon(self):
        return self.lift_motor

    def initSensor(self):
        self.lift_motor.selectProfileSlot(0,0)
        self.lift_motor.setQuadraturePosition(0)

    state_table = {
        "manual_up":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.PercentOutput,
                    -.5
                ),
        "manual_down":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.PercentOutput,
                    .25
                ),
        "manual_stop":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.PercentOutput,
                    -0.05
                ),
        "hatch_bottom":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.Position,
                    self.POSITION_HATCH_BOTTOM
                ),
        "hatch_middle":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.Position,
                    self.POSITION_HATCH_MIDDLE
                ),
        "hatch_top":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.Position,
                    self.POSITION_HATCH_TOP
                ),
        "ball_bottom":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.Position,
                    self.POSITION_BALL_BOTTOM
                ),
        "ball_middle":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.Position,
                    self.POSITION_BALL_MIDDLE
                ),
        "ball_top":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.Position,
                    self.POSITION_BALL_TOP
                )
    }

    def update(self):
        if self.ball_bottom.get():
            self.state = "ball_bottom"
        elif self.ball_middle.get():
            self.state = "ball_middle"
        elif self.ball_top.get():
            self.state = "ball_top"
        elif self.hatch_bottom.get():
            self.state = "hatch_bottom"
        elif self.hatch_middle.get():
            self.state = "hatch_middle"
        elif self.hatch_top.get():
            self.state = "hatch_top"

        if self.manual_up.get():
            self.state = "manual_up"
        elif self.manual_down.get():
            self.state = "manual_down"
        elif self.state is "manual_up" or self.state is "manual_down":
            self.state = "manual_stop"

        self.state_table[self.state](self)

    def log(self):
        wpilib.SmartDashboard.putString("lift_state", self.state)
        wpilib.SmartDashboard.putNumber("lift_position", self.lift_motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber("lift_velocity", self.lift_motor.get())
        wpilib.SmartDashboard.putBoolean("manual_up_button", self.manual_up.get())
        wpilib.SmartDashboard.putBoolean("manual_down_button", self.manual_down.get())
        wpilib.SmartDashboard.putBoolean("ball_bottom_button", self.ball_bottom.get())
        wpilib.SmartDashboard.putBoolean("ball_middle_button", self.ball_middle.get())
        wpilib.SmartDashboard.putBoolean("ball_top_button", self.ball_top.get())
        wpilib.SmartDashboard.putBoolean("hatch_bottom_button", self.hatch_bottom.get())
        wpilib.SmartDashboard.putBoolean("hatch_middle_button", self.hatch_middle.get())
        wpilib.SmartDashboard.putBoolean("hatch_top_button", self.hatch_top.get())
