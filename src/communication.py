import RPi.GPIO as GPIO
import time
import threading

# Candy selections
CANDY1 = 0
CANDY2 = 1

# Pin configuration
_PIN_IN_CANDY_DONE = 33

_PIN_OUT_CANDY1 = 37
_PIN_OUT_CANDY2 = 35

# Delay configuration
DELAY_PIN_TOGGLE_S = 0.75
DELAY_RESP_WAIT_S = 1
DELAY_TIMEOUT_S = 20

# Thread for processing
_THREAD_WAITING_SIGNAL = None

# Return values for requests
RESPONSE_TIMEOUT = 0
RESPONSE_SUCCESS = 1

def setup_communication():
    print("Setting up GPIO pins...")

    GPIO.setmode(GPIO.BOARD)

    # Pin directions
    GPIO.setup(_PIN_OUT_CANDY1, GPIO.OUT)
    GPIO.setup(_PIN_OUT_CANDY2, GPIO.OUT)
    GPIO.setup(_PIN_IN_CANDY_DONE, GPIO.IN)

    # Initial values
    GPIO.output(_PIN_OUT_CANDY1, GPIO.LOW)
    GPIO.output(_PIN_OUT_CANDY2, GPIO.LOW)
    
def close_communication():
    print("Cleaning up GPIO pins...")

    GPIO.cleanup()

def request_candy(candy, ready_callback):
    global _THREAD_WAITING_SIGNAL, _STOP_THREAD
    if _THREAD_WAITING_SIGNAL is not None and _THREAD_WAITING_SIGNAL.is_alive():
        # Waits for the current thread to stop
        print("Current candy request has not been finished, ignoring request")
        return

    if candy == CANDY1:
        req_pin = _PIN_CANDY1
    elif candy == CANDY2:
        req_pin = _PIN_CANDY2
    else:
        raise ValueError("Invalid candy")

    # Creates thread in the background and waits for the robot response
    _THREAD_WAITING_SIGNAL = threading.Thread(target=_communicate, args=(req_pin,ready_callback), daemon=True)
    _THREAD_WAITING_SIGNAL.start()

def _communicate(candy_req_pin, ready_callback):
    print('Waiting for candy...')
    response = _wait_signal(candy_req_pin, _PIN_IN_CANDY_DONE, DELAY_TIMEOUT_S)
    return ready_callback(response)

def _wait_signal(req_pin, resp_pin, timeout_s):
    # Turn on and off pin
    print(f'Toggling request pin:{req_pin}...')
    GPIO.output(req_pin, GPIO.HIGH)
    time.sleep(DELAY_PIN_TOGGLE)
    GPIO.output(req_pin, GPIO.LOW)

    time_started = time.time()
    print(f'Waiting response pin:{resp_pin}...')

    while True:
        # Handles timeout
        time_current = time.time()
        if time_current > time_started + timeout_s:
            print(f'Response pin:{resp_pin} timed out...')
            return RESPONSE_TIMEOUT

        resp = GPIO.input(resp_pin)
        # output signal is reversed due to voltage converter
        if resp == GPIO.LOW:
            print(f'Response received from pin:{resp_pin}...')
            return RESPONSE_SUCCESS

        # wait time, to reduce CPU usage
        time.sleep(DELAY_RESP_WAIT)
