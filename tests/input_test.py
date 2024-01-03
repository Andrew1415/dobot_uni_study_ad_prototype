import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

out_pin = 31
in_pin = 33

GPIO.setup(out_pin, GPIO.OUT)
GPIO.setup(in_pin, GPIO.IN)

DELAY = 2
val = True

try:
    while True:
        if val:
            GPIO.output(out_pin, GPIO.HIGH)
        else:
            GPIO.output(out_pin, GPIO.LOW)

        res = GPIO.input(in_pin)
        print(f"Expected: {val}, Received: {res}")
        val = not val
        time.sleep(DELAY)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
