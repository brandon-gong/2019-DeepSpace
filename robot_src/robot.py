import wpilib
import wpilib.drive
import rev
from ctre import WPI_TalonSRX

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick = wpilib.Joystick(0)
        self.frontLeft  = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.frontRight = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.rearLeft   = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.rearRight  = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.lift = WPI_TalonSRX(3)
        self.drive = wpilib.drive.MecanumDrive(
            self.frontLeft,
            self.rearLeft,
            self.frontRight,
            self.rearRight)

    def teleopPeriodic(self):
        self.drive.driveCartesian(self.stick.getRawAxis(1), 0, self.stick.getRawAxis(2))
        self.lift.set(WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getRawAxis(0));

if __name__ == "__main__":
    wpilib.run(MyRobot)
