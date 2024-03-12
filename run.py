from src import gui

def main():
    try:
        #setup_communication()
        gui.setup_window()
    except Exception as e:
        raise
    finally:
        pass
        #close_communication()

if __name__ == "__main__":
    main()
