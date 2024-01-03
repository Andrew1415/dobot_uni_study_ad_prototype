import RPi.GPIO as GPIO
import time

led_pin = 37
led_pin2 = 31
led_pin3 = 33
GPIO.setmode(GPIO.BOARD)

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)
GPIO.setup(led_pin3, GPIO.OUT)

DELAY = 2

def switch_led(pin):
    print(f"Turning on pin {pin}")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(DELAY)  # Wait for 1 second

    print(f"Turning off pin {pin}")
    # Turn off the LED
    GPIO.output(pin, GPIO.LOW)
    time.sleep(DELAY)  # Wait for 1 second

try:
    while True:
        switch_led(led_pin)
        switch_led(led_pin2)
        switch_led(led_pin3)

except KeyboardInterrupt:
    pass

finally:
    # Cleanup GPIO on script exit
    GPIO.cleanup()