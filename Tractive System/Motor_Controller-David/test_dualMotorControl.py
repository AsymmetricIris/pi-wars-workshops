import DualMotorController as DMC

motorControl = DMC.DualMotorController(24, 23, 25, 18, 15, 14, 0, 0)

try:
    while True:
        motorControl.drive(55, 0)

except KeyboardInterrupt:
    # press ctrl-c in the terminal to end
    # motor ctrl with the program
    motorControl.powerDown()