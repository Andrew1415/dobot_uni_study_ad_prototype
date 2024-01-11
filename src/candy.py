import RPi.GPIO as GPIO
import time
from threading import Thread

FORTUNA = "fortuna"
ANANASAS = "ananasas"

_FORTUNA_PIN = 37
_ANANASAS_PIN = 35
_READY_PIN = 33

_THREAD_WAITING: Thread = None
_STOP_THREAD = False

def setup_communication():
    print("Setting up GPIO pins...")

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(_FORTUNA_PIN, GPIO.OUT)
    GPIO.setup(_ANANASAS_PIN, GPIO.OUT)
    GPIO.setup(_READY_PIN, GPIO.IN)

    # Initial values
    GPIO.output(_FORTUNA_PIN, GPIO.LOW)
    GPIO.output(_ANANASAS_PIN, GPIO.LOW)
    
def close_communication():
    print("Cleaning up GPIO pins...")

    GPIO.cleanup()

def request_candy(candy, ready_callback):
    # Terminate current thread if there is one running
    global _THREAD_WAITING, _STOP_THREAD
    if _THREAD_WAITING is not None and _THREAD_WAITING.is_alive():
        # Waits for the current thread to stop
        print("Current candy request has not been finished, aborting the current one")
        _STOP_THREAD = True
        _THREAD_WAITING.join()
        _STOP_THREAD = False

    if candy == FORTUNA:
        req_pin = _FORTUNA_PIN
    elif candy == ANANASAS:
        req_pin = _ANANASAS_PIN
    else:
        raise ValueError("Invalid candy")

    print(f"Requesting new candy {candy}...")

    # Creates thread in the background and waits for the robot response
    _THREAD_WAITING = Thread(target=_wait_candy, args=(req_pin,ready_callback,))
    _THREAD_WAITING.start()

def _wait_candy(req_pin, ready_callback):
    GPIO.output(req_pin, GPIO.HIGH)
    received_output = False

    while not _STOP_THREAD:
        res = GPIO.input(_READY_PIN)
        # output signal is reversed due to voltage converter
        if res == GPIO.LOW:
            print("Robot signal received!")
            received_output = True
            break

    GPIO.output(req_pin, GPIO.LOW)

    if received_output:
        return ready_callback()