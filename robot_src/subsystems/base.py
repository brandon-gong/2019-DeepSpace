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
import wpilib.drive
from wpilib.buttons import JoystickButton

# Base subsystem code.
# Controls the mecanum drive motors, taking input from the joystick and the
# NavX. Position and velocity control are not implemented.
class Base():

    # Initialize a new instance of Base.
    # @param fl, rl, fr, rr - the front-left, rear-left, front-right, rear-right
    # motors of the drive base, respectively.
    # @param navx - the NavX instance.
    # @param stick - the Joystick instance.
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
        self.foctoggledown = False

    # Ignore all joystick inputs that are below a certain threshold.
    def deadband(self, val):
        if abs(val) < .2:
            val = 0
        return val

    # Update the mecanum drive and FOC status.
    def update(self):

        # You *cannot* use a simple if statement without the helper focenabled
        # variable to toggle FOC state.
        if self.foctoggle.get() and not self.foctoggledown:
            self.focenabled = not self.focenabled
            self.foctoggledown = True
        elif not self.foctoggle.get() and self.foctoggledown:
            self.foctoggledown = False

        scaleval = (1 - self.stick.getThrottle()) * 0.8 + 0.1
        # Based on FOC state, decide whether or not to pass NavX heading.
        if self.focenabled:
            self.drive.driveCartesian(
                self.deadband(self.stick.getX()) * scaleval * 2,
                -self.deadband(self.stick.getY()) * scaleval,
                self.stick.getZ()*0.25 * scaleval,
                self.navx.getAngle()
            )
        else:
            self.drive.driveCartesian(
                self.deadband(self.stick.getX()) * scaleval * 2,
                -self.deadband(self.stick.getY()) * scaleval,
                self.stick.getZ()*0.25 * scaleval
            )

    # Log as much data as possible to SmartDashboard for debug purposes.
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
