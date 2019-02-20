# Copyright (c) 2019 Dragon Robotics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from ctre import WPI_TalonSRX
from wpilib.buttons import JoystickButton
import wpilib

# Lift subsystem code.
# The lift is implemented as one large state machine, controlling the lift
# between PercentOutput and Positional control modes.
class Lift():

    # Encoder constants for the lift.
    # TODO recalibrate.
    POSITION_MAX          = -6.624 * (10**4)
    POSITION_HATCH_TOP    = -6.300 * (10**4)
    POSITION_HATCH_MIDDLE = -3.022 * (10**4)
    POSITION_HATCH_BOTTOM =  0.000

    POSITION_BALL_TOP     = -6.400 * (10**4)
    POSITION_BALL_MIDDLE  = -4.735  * (10**4)
    POSITION_BALL_BOTTOM  = -2.323 * (10**4)

    POSITION_HUMAN_PLAYER = -3.993 * (10**4)

    # Initialize a new Lift instance.
    # @param lift_talon - the motor for the lift.
    # @param upper_switch - the upper limit switch.
    # @param lower_switch - the lower limit switch.
    # @param stick - the Joystick instance.
    def __init__(self, lift_talon, upper_switch, lower_switch, stick):

        self.lift_motor = lift_talon
        self.upper_switch = upper_switch
        self.lower_switch = lower_switch

        # I don't think there's a better way to do this. Using an array will
        # sacrifice too much readability for not much more conciseness.
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

    # Rezero lift_motor encoder and tell it to use the 1st PID slot
    def initSensor(self):
        self.lift_motor.selectProfileSlot(0,0)
        self.lift_motor.setQuadraturePosition(0)

    # Large table with all of the states.  This is a dictionary that will let
    # you look up functions by the name of the state.
    state_table = {
        "manual_up":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.PercentOutput,
                    -.60
                ),
        "manual_down":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.PercentOutput,
                    .25
                ),
        "manual_stop":
            lambda self: self.lift_motor.set(
                    WPI_TalonSRX.ControlMode.PercentOutput,
                    -0.02
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

    # update the lift.
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

        # Manual up and down MUST OVERRIDE all of the auto lift states.
        if self.manual_up.get():
            self.state = "manual_up"
        elif self.manual_down.get():
            self.state = "manual_down"
        elif self.state is "manual_up" or self.state is "manual_down":
            self.state = "manual_stop"

        # limit switch checks.  If a limit switch is pressed, rezero the
        # encoder and go into manual_stop state.
        if not self.upper_switch.get():
            self.lift_motor.setQuadraturePosition(int(self.POSITION_MAX))
            if self.lift_motor.get() < -0.05 or self.state is "manual_up":
                self.lift_motor.set(
                        WPI_TalonSRX.ControlMode.PercentOutput,
                        0
                )
                self.state = "manual_stop"
                return
        if not self.lower_switch.get():
            self.lift_motor.setQuadraturePosition(0)
            if self.lift_motor.get() > 0.05 or self.state is "manual_down":
                self.lift_motor.set(
                        WPI_TalonSRX.ControlMode.PercentOutput,
                        0
                )
                self.state = "manual_stop"
                return

        # execute the state.
        self.state_table[self.state](self)

    # Log as much data as possible to SmartDashboard.
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
        wpilib.SmartDashboard.putBoolean("upper_limit", self.upper_switch.get())
        wpilib.SmartDashboard.putBoolean("lower_limit", self.lower_switch.get())
