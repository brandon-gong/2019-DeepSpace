import wpilib
from navx import AHRS
from wpilib.buttons import JoystickButton
import rev
from ctre import WPI_TalonSRX
from networktables import NetworkTables

from subsystems import *


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
