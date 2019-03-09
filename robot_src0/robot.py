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

# The main class for robot code.  This is the central entry point of the
# robot's code execution. Here, all subsystems are initialized, updated, and
# logged in a loop while the robot is running.  There should not be anything
# other than that in this file.  All code for actually moving parts should be in
# a corresponding subsystem file.
class MyRobot(wpilib.TimedRobot):

    # Called once on robot startup.
    # Declare and initialize the joystick and all of the subsystems.
    # More documentation on each of these constructors is present in their file.
    def robotInit(self):

        wpilib.CameraServer.launch()
        self.stick = wpilib.Joystick(0)
        self.base = Base(
            rev.CANSparkMax(4, rev.MotorType.kBrushless),
            rev.CANSparkMax(2, rev.MotorType.kBrushless),
            rev.CANSparkMax(3, rev.MotorType.kBrushless),
            rev.CANSparkMax(1, rev.MotorType.kBrushless),
            AHRS.create_spi(wpilib.SPI.Port.kMXP),
            self.stick
        )
        self.lift = Lift(WPI_TalonSRX(3), wpilib.DigitalInput(0), wpilib.DigitalInput(1), self.stick)
        self.arm = Arm(
            wpilib.Solenoid(5,2),
            wpilib.Solenoid(5,4),
            wpilib.Solenoid(5,1),
            wpilib.Solenoid(5,5),
            self.stick
        )
        self.ballintake = BallIntake(WPI_TalonSRX(4))
        self.ledController = LEDController.getInstance()
        self.ledController.setState(5002)
        # Various one-time initializations happen here.
        self.lift.initSensor()
        self.base.navx.reset()
        NetworkTables.initialize()
        self.visiontable = NetworkTables.getTable("visiontable")
        self.lights = False
        self.op = False

        self.roller = Roller(WPI_TalonSRX(20), WPI_TalonSRX(10), self.stick, "init")

    # Called repeatedly in a loop while the robot is disabled.
    def disabledPeriodic(self):

        if wpilib.DriverStation.getInstance().getAlliance() == wpilib.DriverStation.Alliance.Blue:
            self.ledController.setState(LEDController.STATE_BLUE_STANDBY)
        elif wpilib.DriverStation.getInstance().getAlliance() == wpilib.DriverStation.Alliance.Red:
            self.ledController.setState(LEDController.STATE_RED_STANDBY)
        else:
            self.ledController.setState(LEDController.STATE_DISABLED)

        self.lift.log()
        self.arm.log()
        self.base.log()
        self.ballintake.log()
        self.roller.log()
        self.ledController.update()
        wpilib.SmartDashboard.putNumber("visionerror", self.visiontable.getNumber("heading_error", 0))

    # Called once on teleop start.
    # Rezero lift encoder and rezero navx heading.
    def teleopInit(self):
        self.lift.initSensor()
        self.base.navx.reset()
        self.roller.state = "init"


    # Called repeatedly during teleop.
    # Update all of the subsystems and log new data to SmartDashboard.
    def teleopPeriodic(self):
        self.base.update()
        self.lift.update()
        self.arm.update()
        self.ballintake.update()
        self.roller.update()
        self.ledController.update()

        self.lift.log()
        self.arm.log()
        self.base.log()
        self.ballintake.log()
        self.roller.log()
        self.ledController.log()


if __name__ == "__main__":
    wpilib.run(MyRobot)
