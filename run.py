from src import gui, communication

def main():
    try:
        communication.setup_communication()
        gui.setup_window()
    except Exception as e:
        raise
    finally:
        communication.close_communication()

if __name__ == "__main__":
    main()
