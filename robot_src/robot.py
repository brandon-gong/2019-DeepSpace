import wpilib
import wpilib.drive
#import wpilib.SensorBase
from wpilib.buttons import JoystickButton
import rev
from lift import Lift
from ctre import WPI_TalonSRX
from networktables import NetworkTables
class MyRobot(wpilib.TimedRobot):

    def robotInit(self):

        self.stick = wpilib.Joystick(0)
        self.frontLeft  = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.frontRight = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.rearLeft   = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.rearRight  = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.lift = Lift(WPI_TalonSRX(3))
        self.othersolenoid = wpilib.Solenoid(5,0)
        self.solenoid = wpilib.Solenoid(5,1)
        self.arm = wpilib.Solenoid(5,2)
        self.otherarm = wpilib.Solenoid(5,3)
        self.stick = wpilib.Joystick(0)
        self.enabled = False
        self.armenabled = False
        self.liftup= JoystickButton(self.stick,3)
        self.liftdown= JoystickButton(self.stick,4)
        self.drive = wpilib.drive.MecanumDrive(
            self.frontLeft,
            self.rearLeft,
            self.frontRight,
            self.rearRight)

        NetworkTables.initialize()
        self.visiontable = NetworkTables.getTable("visiontable")

    def teleopInit(self):
        self.solenoid.set(True)
        self.othersolenoid.set(False)
        self.arm.set(True)
        self.otherarm.set(False)

    def teleopPeriodic(self):
        #self.drive.driveCartesian(self.stick.getX(), -self.stick.getY(), self.stick.getZ()*0.25)
        #self.lift.set(WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getRawAxis(0));
        #wpilib.SmartDashboard.putNumber("tapeerror", self.visiontable.getNumber("heading_error", -300000))
        if self.liftup.get():
            self.lift.up()
        elif self.liftdown.get():
            self.lift.down()
        else:
            self.lift.stop()
        print(self.visiontable.getNumber("heading_error", 0))

        if self.stick.getButton(1) == True and self.enabled == False:
            self.enabled = True
            self.solenoid.set(not self.solenoid.get())
            self.othersolenoid.set(not self.othersolenoid.get())
        elif self.stick.getButton(1) == False and self.enabled:
            self.enabled = False

        if self.stick.getButton(2) == True and self.armenabled == False:
            self.armenabled = True
            self.arm.set(not self.arm.get())
            self.otherarm.set(not self.otherarm.get())
        elif self.stick.getButton(2) == False and self.armenabled:
            self.armenabled = False





if __name__ == "__main__":
    wpilib.run(MyRobot)
