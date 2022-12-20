import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(40,IO.IN) #GPIO 14 -> IR sensor as input

while 1:

    if(IO.input(40)==True): #object is black
        print("The object is black")
        time.sleep(0.5)
    
    if(IO.input(40)==False): #object is white
        print("The object is white")
        time.sleep(0.5)