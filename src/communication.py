import RPi.GPIO as GPIO
import time
import threading

CANDY1 = "candy1"
CANDY2 = "candy2"

_PIN_CANDY1 = 37
_PIN_CANDY2 = 35
_READY_PIN = 33
DELAY_PIN_TOGGLE = 0.75

DELAY_RESP_WAIT = 1
_THREAD_WAITING: threading.Thread = None
_STOP_THREAD = False

def setup_communication():
    print("Setting up GPIO pins...")

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(_PIN_CANDY1, GPIO.OUT)
    GPIO.setup(_PIN_CANDY2, GPIO.OUT)
    GPIO.setup(_READY_PIN, GPIO.IN)

    # Initial values
    GPIO.output(_PIN_CANDY1, GPIO.LOW)
    GPIO.output(_PIN_CANDY2, GPIO.LOW)
    
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

    if candy == CANDY1:
        req_pin = _PIN_CANDY1
    elif candy == CANDY2:
        req_pin = _PIN_CANDY2
    else:
        raise ValueError("Invalid candy")

    print(f"Requesting new candy {candy}...")

    # Creates thread in the background and waits for the robot response
    _THREAD_WAITING = threading.Thread(target=_communicate, args=(req_pin,ready_callback,))
    _THREAD_WAITING.start()

def _communicate(candy_req_pin, ready_callback):
    _wait_signal(candy_req_pin, _READY_PIN)
    return ready_callback()

def _wait_signal(req_pin, resp_pin):
    # Turn on and off candy pin
    GPIO.output(req_pin, GPIO.HIGH)
    time.sleep(DELAY_PIN_TOGGLE)
    GPIO.output(req_pin, GPIO.LOW)

    while not _STOP_THREAD:
        res = GPIO.input(resp_pin)
        # output signal is reversed due to voltage converter
        if res == GPIO.LOW:
            return

        # wait time, to reduce CPU usage
        time.sleep(DELAY_RESP_WAIT)
