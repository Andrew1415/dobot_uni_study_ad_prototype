import RPi.GPIO as GPIO
import time
from threading import Thread

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

    # Initial values
    GPIO.output(_FORTUNA_PIN, GPIO.LOW)
    GPIO.output(_ANANASAS_PIN, GPIO.LOW)
    

def request_candy(candy, ready_callback):
    print(f"Requesting candy {candy}...")

    if candy == FORTUNA:
        req_pin = _FORTUNA_PIN
    elif candy == ANANASAS:
        req_pin = _ANANASAS_PIN
    else:
        raise ValueError("Invalid candy")


    t1 = Thread(target=_wait_candy, args=(req_pin,ready_callback,))
    t1.start()

def _wait_candy(req_pin, ready_callback):
    GPIO.output(req_pin, GPIO.HIGH)

    while True:
        print("Waiting for robot input...")
        res = GPIO.input(_READY_PIN)
        # output is reversed due to voltage converter
        if not res:
            print("Robot signal received!")
            ready_callback()
            break

        time.sleep(CHECK_DELAY)

    GPIO.output(req_pin, GPIO.LOW)

setup_gpio()