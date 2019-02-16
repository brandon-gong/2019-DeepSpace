import wpilib
from ctre import WPI_TalonSRX

class BallIntake():

    def __init__(self, motor):
        self.motor = motor

    def update(self):
        if wpilib.DriverStation.getInstance().getStickPOV(0, 0) == -1:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 0:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 1)
        elif wpilib.DriverStation.getInstance().getStickPOV(0, 0) == 180:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, -1)

    def log(self):
        wpilib.SmartDashboard.putNumber("stickpov", wpilib.DriverStation.getInstance().getStickPOV(0, 0))
        wpilib.SmartDashboard.putNumber("ballintake_speed", self.motor.get())
