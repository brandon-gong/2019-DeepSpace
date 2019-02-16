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
from navx import AHRS
from wpilib.buttons import JoystickButton
import rev
from ctre import WPI_TalonSRX
from networktables import NetworkTables

from subsystems import *

# The main class for robot code.
class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick = wpilib.Joystick(0)
        self.lift = Lift(WPI_TalonSRX(3), self.stick)
        self.arm = Arm(
            wpilib.Solenoid(5,1),
            wpilib.Solenoid(5,0),
            wpilib.Solenoid(5,2),
            wpilib.Solenoid(5,3),
            self.stick
        )
        self.base = Base(
            rev.CANSparkMax(4, rev.MotorType.kBrushless),
            rev.CANSparkMax(2, rev.MotorType.kBrushless),
            rev.CANSparkMax(3, rev.MotorType.kBrushless),
            rev.CANSparkMax(1, rev.MotorType.kBrushless),
            AHRS.create_spi(wpilib.SPI.Port.kMXP),
            self.stick
        )
        self.ballintake = BallIntake(WPI_TalonSRX(4))

        self.lift.initSensor()
        self.base.navx.reset()
        NetworkTables.initialize()
        self.visiontable = NetworkTables.getTable("visiontable")

    def disabledPeriodic(self):
        self.lift.log()
        self.arm.log()
        self.base.log()
        self.ballintake.log()

    def teleopInit(self):
        self.lift.initSensor()
        self.base.navx.reset()

    def teleopPeriodic(self):
        self.lift.update()
        self.arm.update()
        self.base.update()
        self.ballintake.update()

        self.lift.log()
        self.arm.log()
        self.base.log()
        self.ballintake.log()


if __name__ == "__main__":
    wpilib.run(MyRobot)
