'''
Created on 27 Feb 2020
 Line following control of 4 Bi-directional Motors 
@author: Calum Thow
# '''

import RPi.GPIO as GPIO
#import RPiSim.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BOARD)


# ================================================================================
# Define constant values and global variables.

# Define the pins for the IR sensors 
irPins = [40,38 ,36]
GPIO.setup(irPins[0],GPIO.IN)
GPIO.setup(irPins[1],GPIO.IN)
GPIO.setup(irPins[2],GPIO.IN)



# Define values for the IR Sensor readings 

irSensorDigital = np.array([0, 0, 0])

threshold = 400 # IR sensor threshold value for line detection

maxSpeed = 255 # the range for speed is(0,255)

# PID control
error = 0.0         # error as a percentage -100 to 0 to 10
output = 0.0        # signal output as a value between -255 to 0 to 255
integrator = 0
derivator = 0.0
derivative = 0.0
integratorMax = 70
integratorMin = -70


REFRESH_INTERVAL = 5 # ms
lastRefreshTime = 0

multiplyer = 0.1          #multiplyer for overall
sP = 50.0           #setpoint as a percentage
kP = 2.5            #proportional multiplyer
kI = 0.3            #integral multiplyer
kD = 16.0            #derivative multiplyer

# binary representation of the sensor reading
# 1 when the sensor detects the line, 0 otherwise
irSensors = [0,0,0]


# A score to determine deviation from the line [-180 ; +180].
# Negative means the robot is left of the line.

errorLast = 0 #  store the last value of error

# ================================================================================
#define PIDController functions


def Scan():
    #Initialise the sensors
    global irSensors
    irSensors = [0,0,0]

    for i in irSensors:
        sensorValue = GPIO.input(irPins[i])
        if sensorValue >= threshold:
            irSensorDigital[i] = 1
        else:
            irSensorDigital[i] = 0
        b = 2-i
        irSensors = irSensors + (irSensorDigital[i]<<b)

def Error():
    #returns the error value for PID control

    #vars
    global error

   #error between -3000 - 0 -3000
    errorLast = error

    #if the line is sorta in the middle
    if (((GPIO.input(irPins[0]) & GPIO.input(irPins[2])) > 100)&( GPIO.input(irPins[1]))>600):
        error = 0.0 - GPIO.input(irPins[0]) + GPIO.input(irPins[2])

    else:
        if (irSensors[0] == 0) & (irSensors[1] == 0) & (irSensors[2] == 0): #no sensor detects the line
            # error decreases as sensor 2 decreases
            if (errorLast < 0):
                error = -1700.0 + GPIO.input(irPins[0])

            #error increases as sensor 0 decreases
            else:
                if (errorLast > 0):
                    error = 1700.0 - GPIO.input(irPins[2])
      
        if (irSensors[0] == 1) & (irSensors[1] == 0) & (irSensors[2] == 0): #left sensor detects the line
            # error decreases as sensor 2 decreases
            error = -1700.0 + GPIO.input(irPins[0]) + GPIO.input(irPins[1])/1.5

        if (irSensors[0] == 1) & (irSensors[1] == 1) & (irSensors[2] == 0): #left sensor and middle detects the line
            # error decreases as sensor 1 increases and sensor 2 decreases
            error = -1700.0 + GPIO.input(irPins[0]) + GPIO.input(irPins[1])

        if (irSensors[0] == 0) & (irSensors[1] == 1) & (irSensors[2] == 0): #never happens threshold too low
            # error decreases as sensor 2 decreases
            error = 0.0 - GPIO.input(irPins[0]) + GPIO.input(irPins[2])

        if (irSensors[0] == 0) & (irSensors[1] == 1) & (irSensors[2] == 1): #right and middle sensors
            error = 1700.0 - GPIO.input(irPins[2]) - GPIO.input(irPins[1])

        if (irSensors[0] == 0) & (irSensors[1] == 0) & (irSensors[2] == 1): #right sensor on the line
             error = 1700.0 - GPIO.input(irPins[2]) - GPIO.input(irPins[1])/1.5
        
        if (irSensors[0] == 1) & (irSensors[1] == 1) & (irSensors[2] == 1): #all sensors 
            #error increases as sensor 0 increases and sensor 2 decreases
            error = 0.0 - GPIO.input(irPins[0]) + GPIO.input(irPins[2])


def Proportional():
    #returns the proprtional results for PID control
    proportional = error * kP
    return proportional

def Integral():
    #returns the integral results for PID control

    #vars
    global integrator
    integral = 0.0


    integrator = integrator + error/10
    if (integrator > (integratorMax/multiplyer)):
        integrator = (integrator/multiplyer)
    else:
        if (integrator < (integratorMin/multiplyer)):
            integrator = (integrator/multiplyer)
    integral = integrator*kI
    return integral


def Derivative():
    #returns the derivative results for PID control

    #vars
    global lastRefreshTime
    global derivator

    if (int(round(time.time()*1000)) - lastRefreshTime >= REFRESH_INTERVAL):
        lastRefreshTime += REFRESH_INTERVAL
        derivative = kD*(error-derivator)
        derivator = error
      
    else:
        derivative = derivative - derivative/10
    return derivative

def PIDController():
    #test
    Error()
    p = Proportional()
    i = Integral()
    d = Derivative()

    c = p +i + d
    output = -c* multiplyer
    return output


def FollowLine():
    #PID controller
    Scan()
    output = PIDController()
    #print(output)
    print("left: ")
    print(GPIO.input(irPins[0]))
 
'todo. call motor controller with output'

while(1):
    FollowLine()
    
    



