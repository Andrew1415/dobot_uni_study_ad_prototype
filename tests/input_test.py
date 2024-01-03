import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

in_pin = 33
GPIO.setup(in_pin, GPIO.IN)

DELAY = 2
try:
    while True:
        res = GPIO.input(in_pin)
        print(res)
        time.sleep(DELAY)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
