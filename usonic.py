#!/usr/bin/python
#
# Copyright 2016 Fork Unstable Media
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#import
import RPi.GPIO as GPIO
import time
import sys
import os, select

# Turn off warnings if you run it a second time...
GPIO.setwarnings(False)

GPIO_SIG = 32 # signal pin
HIT_DISTANCE = 20.0 # distance when target hit
MAX_DISTANCE = 60.0 # max distance
MIN_DISTANCE = 1.0 #minimum distance
SOUND_SPEED = 34300.0 # cm/s
SETTLE_BREAK = 0.03 # 0.03 default
PULSE = 0.0002 # 0.0001 default
HIT_CALL_SLEEP = 0.1

OLD = 0 # old value

def Measure():
    # setup the GPIO_SIG as output
    GPIO.setup(GPIO_SIG, GPIO.OUT)

    # Set Trigger to LOW
    GPIO.output(GPIO_SIG, GPIO.LOW)
    # Module Settle break
    time.sleep(SETTLE_BREAK)

    # Send signal
    GPIO.output(GPIO_SIG, GPIO.HIGH)
    time.sleep(PULSE)
    GPIO.output(GPIO_SIG, GPIO.LOW)
    start = time.time()

    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while GPIO.input(GPIO_SIG) == 0:
        start = time.time()

    #
    max_stop_time = start + ( MAX_DISTANCE * 2 / SOUND_SPEED )
    stop = time.time()

    while GPIO.input(GPIO_SIG) == 1 and stop < max_stop_time:
        stop = time.time()

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = ( ( stop - start ) * SOUND_SPEED / 2.0 )

    return distance


# Main program loop
if len(sys.argv) > 1:
    arguments = sys.argv[1].lower().split(',')
    if len(arguments) != 5:
        print "Bad number of arguments supplied"
        print arguments
        sys.exit(0)

    GPIO_SIG        = int(arguments[0])
    HIT_DISTANCE    = float(arguments[1])
    MAX_DISTANCE    = float(arguments[2])
    MIN_DISTANCE    = float(arguments[3])    
    HIT_CALL_SLEEP  = float(arguments[4])

    GPIO.setmode(GPIO.BOARD)        # Use GPIO BOARD numbers

    # Flush stdin so we start clean
    while len(select.select([sys.stdin.fileno()], [], [], 0.0)[0])>0:
        os.read(sys.stdin.fileno(), 4096)

    while True:
        try:
            distance = Measure()
            dis_round = int(distance)+0.5
            if dis_round != OLD:
                if distance < HIT_DISTANCE and distance > MIN_DISTANCE:
                    print "%.2f" % distance
                OLD = dis_round
                time.sleep(HIT_CALL_SLEEP)

        except:                     # try to clean up on exit
            print("0.0");
            GPIO.cleanup(GPIO_SIG)
            sys.exit(0)

else:
    print "Bad params"
    print "    sudo usonic.py signal,hit_distance,max_distance,min_distance,hit_sleep"
    sys.exit(0)
