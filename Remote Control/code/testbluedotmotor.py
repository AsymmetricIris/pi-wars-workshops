from bluedot import BlueDot
import RPi.GPIO as GPIO          
from time import sleep
from signal import pause

bd = BlueDot()

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
pA.start(25)
pB=GPIO.PWM(enB,1000)#enA port
pB.start(14) #enB port
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    
print("high")
pA.ChangeDutyCycle(100)
pB.ChangeDutyCycle(100)
def dpad(pos):
    if pos.top:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        print("forward")
    
    elif pos.bottom:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        print("backward")
        print("down")
    elif pos.left:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        print("left")
    elif pos.right:
        print("right")
    elif pos.middle:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        print("stop")
        print("fire")
bd.when_pressed = dpad
pause()