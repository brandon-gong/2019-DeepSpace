from ctre import WPI_TalonSRX
from wpilib.buttons import JoystickButton
import wpilib

class Lift():

    POSITION_MAX          = -6.624 * (10**4)
    POSITION_HATCH_TOP    = -6.624 * (10**4)
    POSITION_HATCH_MIDDLE = -3.547 * (10**4)
    POSITION_HATCH_BOTTOM =  0.000

    POSITION_BALL_TOP     = -6.324 * (10**4)
    POSITION_BALL_MIDDLE  = -0.000 * (10**4)
    POSITION_BALL_BOTTOM  = -0.000 * (10**4)

    POSITION_HUMAN_PLAYER = -0.000 * (10**4)

    def __init__(self,liftTalon,stick):
        self.lift = liftTalon

        self.manual_up = JoystickButton(stick, 3)
        self.manual_down = JoystickButton(stick, 4)
        self.ball_bottom = JoystickButton(stick, 5)
        self.ball_middle = JoystickButton(stick, 6)
        self.ball_top = JoystickButton(stick, 7)
        self.hatch_bottom = JoystickButton(stick, 10)
        self.hatch_middle = JoystickButton(stick, 9)
        self.hatch_top = JoystickButton(stick, 8)

        self.state = "manual_stop"

    def getTalon(self):
        return self.lift

    def state_manual_up(self):
        self.lift.set(WPI_TalonSRX.ControlMode.PercentOutput,-.5)
    def state_manual_down(self):
        self.lift.set(WPI_TalonSRX.ControlMode.PercentOutput,.25)
    def state_manual_stop(self):
        self.lift.set(WPI_TalonSRX.ControlMode.PercentOutput,-0.05)
    def state_ball_bottom(self):
        self.lift.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_BALL_BOTTOM)
    def state_ball_middle(self):
        self.lift.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_BALL_MIDDLE)
    def state_ball_top(self):
        self.lift.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_BALL_TOP)
    def state_hatch_bottom(self):
        self.lift.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_HATCH_BOTTOM)
    def state_hatch_middle(self):
        self.lift.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_HATCH_MIDDLE)
    def state_hatch_top(self):
        self.lift.set(WPI_TalonSRX.ControlMode.Position, self.POSITION_HATCH_TOP)

    state_table = {
        "manual_up" : state_manual_up,
        "manual_down" : state_manual_down,
        "manual_stop" : state_manual_stop,
        "hatch_bottom" : state_hatch_bottom,
        "hatch_middle" : state_hatch_middle,
        "hatch_top" : state_hatch_top,
        "ball_bottom" : state_ball_bottom,
        "ball_middle" : state_ball_middle,
        "ball_top" : state_ball_top
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
        wpilib.SmartDashboard.putString("liftstate", self.state)
