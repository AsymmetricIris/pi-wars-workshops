import RPi.GPIO as GPIO          
from time import sleep

#Motor one
in1 = 24 
in2 = 23
enA = 25
temp1=1
#Motor two
in3 = 18
in4= 17
enB = 27
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

GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.HIGH)
GPIO.output(in4,GPIO.LOW)
pA.ChangeDutyCycle(100)
pB.ChangeDutyCycle(100)