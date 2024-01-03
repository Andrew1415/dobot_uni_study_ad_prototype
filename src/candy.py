import RPi.GPIO as GPIO
import time

FORTUNA = "fortuna"
ANANASAS = "ananasas"

_FORTUNA_PIN = 37
_ANANASAS_PIN = 35
_READY_PIN = 33

CHECK_DELAY = 1

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

    print(f"Requesting candy {candy}...")
    GPIO.output(req_pin, GPIO.HIGH)

    while True:
        print("Waiting for robot input...")
        res = GPIO.input(_READY_PIN)
        if res:
            print("Robot signal received!")
            ready_callback()
            return

        time.sleep(CHECK_DELAY)

setup_gpio()