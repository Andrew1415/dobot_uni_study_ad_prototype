from src import gui, communication
import logging

def main():
    logging.basicConfig(level=logging.INFO)

    try:
        communication.setup_communication()
        gui.setup_window()
    except Exception as e:
        logging.exception(e)
    finally:
        communication.close_communication()

if __name__ == "__main__":
    main()
