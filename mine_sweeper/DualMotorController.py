import DcMotor as DCM
import RPi.GPIO as GPIO

class DualMotorController(object):
    def __init__(self, m1_pin_in1, m1_pin_in2, m1_pin_pwm, 
            m2_pin_in1, m2_pin_in2, m2_pin_pwm, m1_pwm, m2_pwm):
        self.m1_pin_in1 = m1_pin_in1
        self.m1_pin_in2 = m1_pin_in2
        self.m1_pin_pwm = m1_pin_pwm
        self.m2_pin_in1 = m2_pin_in1
        self.m2_pin_in2 = m2_pin_in2
        self.m2_pin_pwm = m2_pin_pwm
        self.m1_pwm = m1_pwm
        self.m2_pwm = m2_pwm
        GPIO.setmode(GPIO.BCM)
        self.motor1 = DCM.DcMotor(m1_pin_in1, m1_pin_in2, m1_pin_pwm, m1_pwm)
        self.motor2 = DCM.DcMotor(m2_pin_in1, m2_pin_in2, m2_pin_pwm, m2_pwm)

    def drive(self, m1_pwm, m2_pwm):
        self.motor1.drive(m1_pwm)
        self.motor2.drive(m2_pwm)

    def halt(self):
        self.drive(0, 0)

    def powerDown(self):
        self.motor1.stop()
        self.motor2.stop()
        GPIO.cleanup()
    
