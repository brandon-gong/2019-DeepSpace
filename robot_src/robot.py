import wpilib
import wpilib.drive
#import wpilib.SensorBase
from navx import AHRS
from wpilib.buttons import JoystickButton
import rev
from lift import Lift
from ctre import WPI_TalonSRX
from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick = wpilib.Joystick(0)
        self.navx = AHRS.create_spi(wpilib.SPI.Port.kMXP)
        self.frontLeft  = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.frontRight = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.rearLeft   = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.rearRight  = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.lift = Lift(WPI_TalonSRX(3), self.stick)
        self.othersolenoid = wpilib.Solenoid(5,0)
        self.solenoid = wpilib.Solenoid(5,1)
        self.arm = wpilib.Solenoid(5,2)
        self.otherarm = wpilib.Solenoid(5,3)
        self.stick = wpilib.Joystick(0)
        self.enabled = False
        self.armenabled = False
        self.liftup= JoystickButton(self.stick,3)
        self.liftdown= JoystickButton(self.stick,4)
        self.focToggle = JoystickButton(self.stick,11)
        self.drive = wpilib.drive.MecanumDrive(
            self.frontLeft,
            self.rearLeft,
            self.frontRight,
            self.rearRight)

        NetworkTables.initialize()
        self.visiontable = NetworkTables.getTable("visiontable")
        self.ballintake = WPI_TalonSRX(4)

    def teleopInit(self):
        self.solenoid.set(True)
        self.othersolenoid.set(False)
        self.arm.set(True)
        self.otherarm.set(False)
        self.lift.getTalon().selectProfileSlot(0,0)
        #self.lift.getTalon().configFeedbackSensor(WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.lift.getTalon().setQuadraturePosition(0)
        self.navx.reset()

    def disabledPeriodic(self):
        wpilib.SmartDashboard.putNumber("position", self.lift.getTalon().getSelectedSensorPosition())

    def deadband(self, val):
        if abs(val) <.2:
            val = 0
        return val

    def teleopPeriodic(self):
        foc_enabled = False
        if self.focToggle.get():
            foc_enabled = not foc_enabled
        if not foc_enabled:
            self.drive.driveCartesian(self.deadband(self.stick.getX())*0.5, -self.deadband(self.stick.getY())*0.5, self.stick.getZ()*0.125)
        elif foc_enabled:
            self.drive.driveCartesian(self.deadband(self.stick.getX())*0.5, -self.deadband(self.stick.getY())*0.5, self.stick.getZ()*0.125, self.navx.getAngle())
        # self.lift.set(WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getRawAxis(0));
        wpilib.SmartDashboard.putNumber("position", self.lift.getTalon().getSelectedSensorPosition())
        # if self.liftup.get():
        #     self.lift.up()
        # elif self.liftdown.get():
        #     self.lift.down()
        # else:
        #      self.lift.stop()

        self.lift.update()
        # print(self.visiontable.getNumber("heading_error", 0))
        #
        # if self.stick.getButton(1) == True and self.enabled == False:
        #     self.enabled = True
        #     self.solenoid.set(not self.solenoid.get())
        #     self.othersolenoid.set(not self.othersolenoid.get())
        # elif self.stick.getButton(1) == False and self.enabled:
        #     self.enabled = False
        #
        # if self.stick.getButton(2) == True and self.armenabled == False:
        #     self.armenabled = True
        #     self.arm.set(not self.arm.get())
        #     self.otherarm.set(not self.otherarm.get())
        # elif self.stick.getButton(2) == False and self.armenabled:
        #     self.armenabled = False
        #
        # if wpilib.DriverStation.getInstance().getStickPOV(0, 0) == -1:
        #     self.ballintake.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        # elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 180:
        #     self.ballintake.set(WPI_TalonSRX.ControlMode.PercentOutput, 1)
        # elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 0:
        #     self.ballintake.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)

        #self.lift.getTalon().set(WPI_TalonSRX.ControlMode.Position, -10000)

if __name__ == "__main__":
    wpilib.run(MyRobot)
