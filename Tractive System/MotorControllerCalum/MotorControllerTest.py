#pi setup
import RPi.GPIO as GPIO          
import time 

#motor Setup
#Motor one
in1 = 24 
in2 = 23
enA = 25
temp1=1
#Motor two
in3 = 18
in4= 15
enB = 14
temp2=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
pA=GPIO.PWM(enA,1000)#enA port
pA.start(enA)
pB=GPIO.PWM(enB,1000)#enA port
pB.start(enB) #enB port
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")

# ================================================================================
#                         motor Balancer

# function to take motor speeds -255 to 255 and attempt to balance them

def Drive(leftSpeed,rightSpeed):
    #offset Additives
    leftOffset = 0.0
    rightOffset = 0.0
    #offset multiplyers
  
    leftMultiplyer = 1.0
    rightMultiplyer = 1.0

    leftSpeed = (leftSpeed+leftOffset)*leftMultiplyer
    rightSpeed = (rightSpeed+rightOffset)*rightMultiplyer
  
    #incase the motor Speed values are out of bounds
    if (leftSpeed > 100):
        leftSpeed = 100

    if (leftSpeed < -100):
        leftSpeed = -100

    if (rightSpeed > 100):
        rightSpeed = 100

    if (rightSpeed < -100):
        rightSpeed = -100


    set_motor_currents(leftSpeed,rightSpeed)

#  ================================================================================
#                         MOTOR CONTROLLER
#  Set the current on a motor channel using PWM and directional logic.
#  Changing the current will affect the motor speed, but please note this is
#  not a calibrated speed control.  This function will configure the pin output
#  state and return.
# 
# param pwm    PWM duty cycle ranging from -255 full reverse to 255 full forward
# param IN1_PIN  pin number xIN1 for the given channel
# param IN2_PIN  pin number xIN2 for the given channel

def set_motor_direction(pwm, IN1_PIN, IN2_PIN, en):

    if (pwm < 0):
        #reverse speeds
        GPIO.output(IN1_PIN,GPIO.LOW)
        GPIO.output(IN2_PIN,GPIO.HIGH)


    else: # stop or forward
        GPIO.output(IN1_PIN,GPIO.HIGH)
        GPIO.output(IN2_PIN,GPIO.LOW)

# // ================================================================================
# /// Set the current on both motors.
# ///
# /// \param pwm_A  motor A PWM, -255 to 255
# /// \param pwm_B  motor B PWM, -255 to 255

def set_motor_currents(pwm_A, pwm_B):

    set_motor_direction(pwm_A, in1, in2, enA)
    set_motor_direction(pwm_B, in3, in4, enB)
    #reverse
    if (pwm_A < 0):
        pA.ChangeDutyCycle(-pwm_A)
    else:
    #forwards
        pA.ChangeDutyCycle(pwm_A)
    
    #reverse
    if (pwm_B < 0):
        pB.ChangeDutyCycle(-pwm_B)
    else:
    #forwards
        pB.ChangeDutyCycle(pwm_B)
    time.sleep(0.2)

# ================================================================================
# Stop PWM on both motors and cleanup for GPIO

def stop_Motors():
    pA.stop()
    pB.stop()
    GPIO.cleanup()