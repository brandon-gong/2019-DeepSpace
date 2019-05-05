<img src="logo.png" align="left" height=100 />

# Deep Space 2019
[![Build Status](https://travis-ci.org/dragonrobotics/2019-DeepSpace.svg?branch=master)](https://travis-ci.org/dragonrobotics/2019-DeepSpace) ![Version](https://img.shields.io/badge/version-v2019.2.1-informational.svg)<br><br>
This repository holds the code developed by Dragon Robotics this year for the 2019 season, Deep Space.  It contains code for the robot, vision processing, custom dashboard, and Arduino LED's.  As of 2/19/19 (stop build day), development has stopped on the `master` branch of this repository.  To view changes post-stop build day, switch over to the `beta` branch.
<br><br>
The repository's code is structured as such:
### `arduino_src`
Contains test code for PWM control of an individually-addressable RGB LED strip via Arduino.  This code communicates over Serial with the RoboRIO and is able to change the display state of the LED's based on serial readings.  We make use of the [FastLED](http://fastled.io/) library for LED control. <br>

### `dashboard_src`
Contains code for the custom dashboard.  We hope that it becomes a continual project that can be reused in later years.  This is a fork of [FRCDashboard](https://github.com/FRCDashboard/FRCDashboard) and runs on Electron and web technologies. <br>
As of stop build day, the custom dashboard is also incomplete.  More work will be done to prepare it for competition day.

### `robot_src`
Contains the main code for the robot. This is probably what you are here to look at.
Our robot code is written in python using [RobotPy](https://robotpy.readthedocs.io/en/stable/).  We have found Python to be a much more convenient, flexible, and simple alternative to Java.  Within the `robot_src` folder, the code is structured in this way:
- `robot.py` is the main entry point of the program.  This is what is actually executed; all other subsystems are imported in and initialized within this file.  If you want to change Talon/Spark ID's, solenoid/digital IO ports, etc., it is likely that you will want to modify this file.
- `subsystems/` contains code for each subsystem on the robot, each one organized into its own file.  A good amount of documentation has been written for each of these files, and more may be added in the future as long as it does not make the file unnecessarily long and hard to edit.
- Each subsystem file is organized into and `__init__()` function, an `update()` function, and a `log()` function.  There may also be other helper functions specific to that subsystem that are implemented.
- If you do not care about implementation details but still want to know how everything is set up so you can makechange if necessary, the `__init__()` function is the right place for you to look.  You will find what arguments in what order are necessary to initialize an object there.
- The `update()` function is called for each subsystem _once_ per `teleopPeriodic()` call and does things like reading inputs and updating motor speeds.  For lift and arm subsystems, this is implemented as a finite state machine, which allows for flexible and overridable behavior within the code.
- The `log()` function outputs statistics and debug information to SmartDashboard and is called _once_ per `disabledPeriodic()` and `teleopPeriodic()`.

### `vision_src`
Contains vision processing code, which runs on the Raspberry Pi and communicates with the robot code over NetworkTables.
The current vision code, while working, does not provide an accurate and stable enough measurement to be used at competition.  It will be modified and improved upon using SIFT/ORB to be more flexible and less susceptible to background noise. <br>
In addition, `vision_src` also contains code for a Java/OpenCV GUI test bed, running on Swing, which allows for relatively fast and live testing and debugging.
