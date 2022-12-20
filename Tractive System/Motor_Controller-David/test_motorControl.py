import MotorControllerTest as MCT
import RPi.GPIO as GPIO

motor = MCT.DcMotor(24, 23, 25, 0)
#motor = MCT.DcMotor(18, 15, 14, 0)

try:
    while True:
        motor.drive(-25)

except KeyboardInterrupt:
    motor.stop()
    GPIO.cleanup()

