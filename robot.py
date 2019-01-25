import wpilib
import wpilib.drive
from ctre import WPI_TalonSRX
from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick = wpilib.Joystick(0)
        fl = WPI_TalonSRX(0)
        fr = WPI_TalonSRX(3)
        bl = WPI_TalonSRX(2)
        br = WPI_TalonSRX(13)
        self.drive = wpilib.drive.MecanumDrive(fl, bl, fr, br)
        self.psolenoid = wpilib.Solenoid(10,1)
        self.solenoid1 = wpilib.Solenoid(10, 5)
        self.solenoid2 = wpilib.Solenoid(10, 0)
        self.ispressed = False
        self.dirispressed = False
        self.pressed = False
        self.cpressed = False
        self.forward = True
        self.roller = WPI_TalonSRX(11)
        NetworkTables.initialize()
        self.visiontable = NetworkTables.getTable("visiontable")
        

    def teleopPeriodic(self):
        if wpilib.DriverStation.getInstance().getStickPOV(0, 0) == -1:
            self.roller.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 0:
            self.roller.set(WPI_TalonSRX.ControlMode.PercentOutput, 1)
        elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 180:
            self.roller.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)
        elif wpilib.DriverStation.getInstance().getStickPOV(0,0) == 90:
            self.forward == True
        elif wpilib.DriverStation.getInstance().getStickPOV(0,0) ==270:
            self.forward == False

        if self.stick.getRawButton(5) == False and self.pressed == True:
            self.pressed = False
        elif self.stick.getRawButton(5) == True and self.pressed == False:
            self.pressed = True
            self.psolenoid.set(not self.psolenoid.get())

     
        
        
            
        if self.forward == True:
            self.drive.driveCartesian(self.stick.getRawAxis(0),-self.stick.getRawAxis(1),self.stick.getRawAxis(2))
        elif self.forward == False:
            self.drive.driveCartesian(-self.stick.getRawAxis(0),self.stick.getRawAxis(1),self.stick.getRawAxis(2))

        
        #if self.ispressed == True and self.stick.getRawButton(1) == False:
        #    self.ispressed = False
        #elif self.ispressed == False and self.stick.getRawButton(1) == True:
        #    self.ispressed = True
        #    self.solenoid1.set(not self.solenoid1.get())
        #    self.solenoid2.set(not self.solenoid2.get())

        self.solenoid1.set(self.visiontable.getNumber("val", 0) == 0)
        self.solenoid2.set(self.visiontable.getNumber("val", 0) == 0)
        
        wpilib.SmartDashboard.putNumber("test", 5.0)

        


if __name__ == "__main__":
    wpilib.run(MyRobot)
