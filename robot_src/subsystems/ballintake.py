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

import wpilib
from ctre import WPI_TalonSRX

# Ball intake subsystem code.
# Currently this code is very simple: run the rollers in and out depending on
# input from POV stick.
class BallIntake():

    # Initialize a new instance of BallIntake.
    # @param motor - An instance of WPI_TalonSRX that represent the motor
    # on the ball intake.
    def __init__(self, motor):
        self.motor = motor

    # Update the BallIntake. Currently up on the POV stick runs the ball intake
    # in, and down on the POV stick runs the ball intake out. Releasing stops
    # the ball intake.
    def update(self):

        # POV values are organized as angles: directly up is 0, directly left is
        # 90, directly down is 180, etc.  Center is -1.
        if wpilib.DriverStation.getInstance().getStickPOV(0, 0) == -1:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 180:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 1)
        elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 0:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)

    # Log values for the BallIntake for debug.
    def log(self):
        wpilib.SmartDashboard.putNumber("stickpov",
            wpilib.DriverStation.getInstance().getStickPOV(0, 0))
        wpilib.SmartDashboard.putNumber("ballintake_speed", self.motor.get())
