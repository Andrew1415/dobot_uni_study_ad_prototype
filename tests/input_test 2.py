import RPi.GPIO as GPIO
import time
import threading

OUT_PINS = [
    [35, False],
    [37, False]
]

IN_PINS = [33]

DELAY = 2

def setup():
    GPIO.setmode(GPIO.BOARD)

    # Pin direction
    for pin in OUT_PINS:
        GPIO.setup(pin[0], GPIO.OUT)

    for pin in IN_PINS:
        GPIO.setup(pin[0], GPIO.IN)

    # Initial states
    for pin in OUT_PINS:
        GPIO.output(pin[0], pin[1])

def resolve_pin(pin):
    return next(x for x in OUT_PINS if x[0] == pin)

def check_in(pin):
    res = GPIO.input(pin)
    print(f"Response from pin{pin}: {res}")

def toggle_out(pin):
    pin[1] = not pin[1]
    GPIO.output(pin[0], pin[1])
    print(f"Toggling pin{pin} to state {'ON' if pin[1] else 'OFF'}")

def log_in_pins():
    while True:
        for pin in IN_PINS:
            check_in(pin)
        time.sleep(DELAY)

def toggle_out_pins():
    while True:
        try:
            pin = resolve_pin(int(input()))
        except:
            continue

        toggle_out(pin)

def main():
    t1 = threading.Thread(target=log_in_pins)
    t2 = threading.Thread(target=toggle_out_pins)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    try:
        main()
    except:
        pass
    finally:
        GPIO.cleanup()