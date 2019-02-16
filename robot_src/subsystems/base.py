import wpilib
import wpilib.drive
from wpilib.buttons import JoystickButton

class Base():
    def __init__(self, fl, rl, fr, rr, navx, stick):
        self.fl = fl
        self.rl = rl
        self.fr = fr
        self.rr = rr
        self.drive = wpilib.drive.MecanumDrive(fl, rl, fr, rr)
        self.navx = navx
        self.stick = stick
        self.foctoggle = JoystickButton(self.stick,11)
        self.focenabled = False

    def deadband(self, val):
        if abs(val) < .1:
            val = 0
        return val

    def update(self):
        if self.foctoggle.get() and not self.focenabled:
            self.focenabled = True
        elif not self.foctoggle.get() and self.focenabled:
            self.focenabled = False
        if self.focenabled:
            self.drive.driveCartesian(
                self.deadband(self.stick.getX()),
                -self.deadband(self.stick.getY()),
                self.stick.getZ()*0.25,
                self.navx.getAngle()
            )
        else:
            self.drive.driveCartesian(
                self.deadband(self.stick.getX()),
                -self.deadband(self.stick.getY()),
                self.stick.getZ()*0.25
            )

    def log(self):
        wpilib.SmartDashboard.putBoolean("foc_enabled", self.focenabled)
        wpilib.SmartDashboard.putNumber("fl_velocity", self.fl.get())
        wpilib.SmartDashboard.putNumber("fr_velocity", self.fr.get())
        wpilib.SmartDashboard.putNumber("rl_velocity", self.rl.get())
        wpilib.SmartDashboard.putNumber("rr_velocity", self.rr.get())
        wpilib.SmartDashboard.putNumber("fl_temperature", self.fl.getMotorTemperature())
        wpilib.SmartDashboard.putNumber("fr_temperature", self.fr.getMotorTemperature())
        wpilib.SmartDashboard.putNumber("rl_temperature", self.rl.getMotorTemperature())
        wpilib.SmartDashboard.putNumber("rr_temperature", self.rr.getMotorTemperature())
        wpilib.SmartDashboard.putNumber("navx_heading", self.navx.getAngle())
        wpilib.SmartDashboard.putNumber("navx_velocity_x", self.navx.getVelocityX())
        wpilib.SmartDashboard.putNumber("navx_velocity_y", self.navx.getVelocityY())
        wpilib.SmartDashboard.putNumber("navx_accel_x", self.navx.getWorldLinearAccelX())
        wpilib.SmartDashboard.putNumber("navx_accel_y", self.navx.getWorldLinearAccelY())
        wpilib.SmartDashboard.putNumber("navx_temp", self.navx.getTempC())
        wpilib.SmartDashboard.putNumber("foc_button", self.foctoggle.get())
        wpilib.SmartDashboard.putNumber("stick_x", self.stick.getX())
        wpilib.SmartDashboard.putNumber("stick_y", self.stick.getY())
        wpilib.SmartDashboard.putNumber("stick_z", self.stick.getZ())
