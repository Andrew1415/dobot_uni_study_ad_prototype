import RPi.GPIO as GPIO
import time

FORTUNA = "fortuna"
ANANASAS = "ananasas"

_FORTUNA_PIN = 37
_ANANASAS_PIN = 35
_READY_PIN = 33

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(_FORTUNA_PIN, GPIO.OUT)
    GPIO.setup(_ANANASAS_PIN, GPIO.OUT)
    GPIO.setup(_READY_PIN, GPIO.IN)


def request_candy(candy, ready_callback):
    if candy == FORTUNA:
        req_pin = _FORTUNA_PIN
    elif candy == ANANASAS:
        req_pin = _ANANASAS_PIN
    else:
        raise ValueError("Invalid candy")
    
    GPIO.output(req_pin, GPIO.high)
    
    led_pin = 37

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
        print(f"Requesting candy {candy}")

def is_candy_ready():
    return False

setup_gpio()