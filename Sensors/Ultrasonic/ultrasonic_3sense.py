import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

# the code uses board pin numbers not Broadcom SOC channel (GPIO) !!!
# Make sure you get note of that


# 1 -> left
# 2 -> center
# 3 -> right

TRIG1 = 16  # GPIO 23
ECHO1 = 18  # GPIO 24

TRIG2 = 7   # GPIO 23
ECHO2 = 11  # GPIO 24

TRIG3 = 13  # GPIO 23
ECHO3 = 15  # GPIO 24

print "Distance Measurement In Progress"

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)

print "waiting for sensor to settle"
time.sleep(2)

# loop
i = 0
while i != 1:
    # send pulse
    GPIO.output(TRIG1, True)
    GPIO.output(TRIG2, True)
    GPIO.output(TRIG3, True)

    time.sleep(0.00001)

    GPIO.output(TRIG1, False)
    GPIO.output(TRIG2, False)
    GPIO.output(TRIG3, False)

    while GPIO.input(ECHO1) == 0:
        pulse1_start = time.time()

    while GPIO.input(ECHO1) == 1:
        pulse1_end = time.time()

    pulse1_duration = pulse1_end - pulse1_start

    while GPIO.input(ECHO2) == 0:
        pulse2_start = time.time()

    while GPIO.input(ECHO2) == 1:
        pulse2_end = time.time()

    pulse2_duration = pulse2_end - pulse2_start

    while GPIO.input(ECHO3) == 0:
        pulse3_start = time.time()

    while GPIO.input(ECHO3) == 1:
        pulse3_end = time.time()

    pulse3_duration = pulse3_end - pulse3_start

    distance1 = rournd(pulse1_duration1 * 17150, 2)
    distance2 = rournd(pulse2_duration1 * 17150, 2)
    distance3 = rournd(pulse3_duration1 * 17150, 2)

    # distance = round(distance, 2)

    print "distance_S1: ", distance1, "cm ", "distance_S2: ", distance2, "cm ", "distance_S2: ", distance2, "cm"
    time.sleep(0.1)
    #i = 1

GPIO.cleanup()
