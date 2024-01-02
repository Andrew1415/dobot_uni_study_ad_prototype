import RPi.GPIO as GPIO
import time

led_pin = 37

GPIO.setup(led_pin, GPIO.OUT)

try:
    # Blink the LED 5 times
    while True:
        # Turn on the LED
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(1)  # Wait for 1 second

        # Turn off the LED
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    pass

finally:
    # Cleanup GPIO on script exit
    GPIO.cleanup()