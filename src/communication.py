import RPi.GPIO as GPIO
import time
import threading
import logging

# Candy selections
CANDY1 = 0
CANDY2 = 1

# Pin configuration
_PIN_IN_CANDY_DONE = 33
_PIN_IN_LEAFLET_DONE = 29

_PIN_OUT_CANDY1 = 37
_PIN_OUT_CANDY2 = 35
_PIN_OUT_LEAFLET = 31


# Delay configuration
DELAY_PIN_TOGGLE_S = 0.75
DELAY_RESP_WAIT_S = 1
DELAY_TIMEOUT_S = 35

# Thread for processing
_THREAD_WAITING_SIGNAL = None

# Return values for requests
RESPONSE_TIMEOUT = 0
RESPONSE_SUCCESS = 1

def setup_communication():
    logging.info("Setting up GPIO pins...")

    GPIO.setmode(GPIO.BOARD)

    # Pin directions
    GPIO.setup(_PIN_OUT_CANDY1, GPIO.OUT)
    GPIO.setup(_PIN_OUT_CANDY2, GPIO.OUT)
    GPIO.setup(_PIN_IN_CANDY_DONE, GPIO.IN)
    GPIO.setup(_PIN_OUT_LEAFLET, GPIO.OUT)
    GPIO.setup(_PIN_IN_LEAFLET_DONE, GPIO.IN)

    # Initial values
    GPIO.output(_PIN_OUT_CANDY1, GPIO.LOW)
    GPIO.output(_PIN_OUT_CANDY2, GPIO.LOW)
    GPIO.output(_PIN_OUT_LEAFLET, GPIO.LOW)

    
def close_communication():
    logging.info("Cleaning up GPIO pins...")

    GPIO.cleanup()

def request_prize(candy, ready_callback):
    global _THREAD_WAITING_SIGNAL, _STOP_THREAD
    if _THREAD_WAITING_SIGNAL is not None and _THREAD_WAITING_SIGNAL.is_alive():
        # Waits for the current thread to stop
        logging.warning("Current candy request has not been finished, ignoring request!")
        return

    if candy == CANDY1:
        req_pin = _PIN_OUT_CANDY1
    elif candy == CANDY2:
        req_pin = _PIN_OUT_CANDY2
    else:
        raise ValueError(f"Invalid request, candy:{candy}")

    # Waits for robot response in the background
    _THREAD_WAITING_SIGNAL = threading.Thread(target=_communicate, args=(req_pin,ready_callback), daemon=True)
    _THREAD_WAITING_SIGNAL.start()

def _communicate(candy_req_pin, ready_callback):
    logging.info('Waiting for candy and leaflet...')
    response = _wait_for_signals((candy_req_pin, _PIN_OUT_LEAFLET), (_PIN_IN_CANDY_DONE, _PIN_IN_LEAFLET_DONE), DELAY_TIMEOUT_S)
    return ready_callback(response)

def _wait_for_signals(req_pins, resp_pins, timeout_s):
    # Turn on and off pin
    for req_pin in req_pins:
        logging.info(f'Toggling request pin:{req_pin} ON...')
        GPIO.output(req_pin, GPIO.HIGH)

    time.sleep(DELAY_PIN_TOGGLE_S)

    for req_pin in req_pins:
        logging.info(f'Toggling request pin:{req_pin} OFF...')
        GPIO.output(req_pin, GPIO.LOW)

    for resp_pin in resp_pins:
        logging.info(f'Waiting response pin:{resp_pin}...')

    time_started = time.time()
    not_responded = set(resp_pins)

    while not_responded:
        # Handle timeout
        time_current = time.time()
        if time_current > time_started + timeout_s:
            for resp_pin in not_responded:
                logging.warning(f'Response pin:{resp_pin} timed out!')
            return RESPONSE_TIMEOUT

        signals = [(resp_pin, GPIO.input(resp_pin)) for resp_pin in not_responded]
        for resp_pin, signal in signals:
            # output signal is reversed due to voltage converter
            if signal == GPIO.LOW:
                logging.info(f'Response pin:{resp_pin} success...')
                not_responded.remove(resp_pin)

        # wait time, to reduce CPU usage
        time.sleep(DELAY_RESP_WAIT_S)

    return RESPONSE_SUCCESS

