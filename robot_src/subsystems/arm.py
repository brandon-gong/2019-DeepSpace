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
from wpilib.buttons import JoystickButton

class Arm():

    def __init__(self, hs1, hs2, as1, as2, stick):
        self.hatchsolenoid1 = hs1
        self.hatchsolenoid2 = hs2
        self.armsolenoid1 = as1
        self.armsolenoid2 = as2

        self.hatchsolenoid1.set(True)
        self.hatchsolenoid2.set(False)
        self.armsolenoid1.set(True)
        self.armsolenoid2.set(False)

        self.hatchbutton = JoystickButton(stick, 1)
        self.armbutton = JoystickButton(stick, 2)
        self.hatchenabled = False
        self.armenabled = False

    def toggleHatch(self):
        self.hatchsolenoid1.set(not self.hatchsolenoid1.get())
        self.hatchsolenoid2.set(not self.hatchsolenoid2.get())

    def toggleArm(self):
        self.armsolenoid1.set(not self.armsolenoid1.get())
        self.armsolenoid2.set(not self.armsolenoid2.get())

    def update(self):
        if self.hatchbutton.get() and not self.hatchenabled:
            self.hatchenabled = True
            self.toggleHatch()
        elif not self.hatchbutton.get() and self.hatchenabled:
            self.hatchenabled = False

        if self.armbutton.get() and not self.armenabled:
            self.armenabled = True
            self.toggleArm()
        elif not self.armbutton.get() and self.armenabled:
            self.armenabled = False

    def log(self):
        wpilib.SmartDashboard.putBoolean("hatchsolenoid1_status", self.hatchsolenoid1.get())
        wpilib.SmartDashboard.putBoolean("hatchsolenoid2_status", self.hatchsolenoid2.get())
        wpilib.SmartDashboard.putBoolean("armsolenoid1_status", self.armsolenoid1.get())
        wpilib.SmartDashboard.putBoolean("armsolenoid2_status", self.armsolenoid2.get())
        wpilib.SmartDashboard.putBoolean("arm_enabled", self.armenabled)
        wpilib.SmartDashboard.putBoolean("hatch_enabled", self.hatchenabled)
        wpilib.SmartDashboard.putBoolean("hatch_button", self.hatchbutton.get())
        wpilib.SmartDashboard.putBoolean("arm_button", self.armbutton.get())
