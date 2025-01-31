import time
import threading
import logging

# Candy selections
CANDY1 = 0
CANDY2 = 1

# Delay configuration
MOCK_DELAY_RESPONSE_S = 5

# Thread for processing
_THREAD_WAITING_SIGNAL = None

# Return values for requests
RESPONSE_TIMEOUT = 0
RESPONSE_SUCCESS = 1

def setup_communication():
    logging.info("Mock: Setting up communication (no actual GPIO setup).")
    
def close_communication():
    logging.info("Mock: Cleaning up communication (no actual GPIO cleanup).")

def request_prize(candy, leaflet, ready_callback):
    global _THREAD_WAITING_SIGNAL
    if _THREAD_WAITING_SIGNAL is not None and _THREAD_WAITING_SIGNAL.is_alive():
        logging.warning("Mock: Current candy request has not been finished, ignoring request!")
        return

    if candy not in (CANDY1, CANDY2):
        raise ValueError(f"Invalid request, candy:{candy}")

    logging.info(f"Mock: Requesting candy {candy}, will respond in {MOCK_DELAY_RESPONSE_S} seconds...")
    _THREAD_WAITING_SIGNAL = threading.Thread(target=_mock_communicate, args=(ready_callback,), daemon=True)
    _THREAD_WAITING_SIGNAL.start()

def _mock_communicate(ready_callback):
    time.sleep(MOCK_DELAY_RESPONSE_S)
    logging.info("Mock: Simulated candy and leaflet success response.")
    ready_callback(RESPONSE_SUCCESS)
