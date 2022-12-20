#pi setup
import RPi.GPIO as GPIO          

class DcMotor(object):
    def __init__(self, pin_in1, pin_in2, pin_Pwm, pwm):
        self.pin_in1 = pin_in1
        self.pin_in2 = pin_in2
        self.pin_Pwm = pin_Pwm
        self.pwm = pwm
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_in1, GPIO.OUT)
        GPIO.setup(pin_in2, GPIO.OUT)
        GPIO.setup(pin_Pwm, GPIO.OUT)
        GPIO.output(pin_in1, GPIO.LOW)
        GPIO.output(pin_in2, GPIO.LOW)
        
        self.pwmControl = GPIO.PWM(pin_Pwm, 1000)
        self.pwmControl.start(pin_Pwm)
    
    def set_Drive_Direction(self, pwm):
        if ( pwm < 0):
            GPIO.output(self.pin_in1, GPIO.LOW)
            GPIO.output(self.pin_in2, GPIO.HIGH)

        else:
            GPIO.output(self.pin_in1, GPIO.HIGH)
            GPIO.output(self.pin_in2, GPIO.LOW)



    def set_pwm(self, newPwm):
        self.pwm = newPwm
    
    def update_pwm(self):
        self.pwmControl.ChangeDutyCycle(self.pwm)

    def drive(self, newPwm):
        if ( self.pwm != newPwm ):
            self.set_Drive_Direction(newPwm)

            if (newPwm < 0): #reverse
                self.set_pwm(-newPwm)
                self.update_pwm()

            else: #forwards
                self.set_pwm(newPwm)
                self.update_pwm()

    def stop(self):
        self.pwmControl.stop()
