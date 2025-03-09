import socket
import threading
import logging
from typing import Callable
from .question_bank import categories, update_statistics

CANDY1: int = 0
CANDY2: int = 1

RESPONSE_TIMEOUT: int = 0
RESPONSE_SUCCESS: int = 1
TCP_TIMEOUT_S: int = 30

IP_CANDY_ROBOT: str = "192.168.2.6"
# IP_CANDY_ROBOT: str = "127.192.1.6"
PORT_CANDY_ROBOT: int = 6001
_CANDY_SOCKET: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_CANDY_SOCKET.settimeout(TCP_TIMEOUT_S)

# IP_LEAFLET_ROBOT: str = "192.168.1.7"
IP_LEAFLET_ROBOT: str = "192.168.2.7"
PORT_LEAFLET_ROBOT: int = 6001
_LEAFLET_SOCKET: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_LEAFLET_SOCKET.settimeout(TCP_TIMEOUT_S)


_EXECUTING_EVENT: threading.Event = threading.Event()


def _connect(robot_socket: socket.socket, ip: str, port: int) -> bool:
    try:
        robot_socket.connect((ip, port))
        logging.info(f"Connected to TCP robot hand {ip}:{port}")
        return True
    except socket.error as e:
        logging.error(
            f"Could not connect to TCP robot hand {ip}:{port}! Error: {e}"
        )
        return False


def setup_communication():
    logging.info("Conneting to robots via TCP...")

    _connect(_CANDY_SOCKET, IP_CANDY_ROBOT, PORT_CANDY_ROBOT)
    _connect(_LEAFLET_SOCKET, IP_LEAFLET_ROBOT, PORT_LEAFLET_ROBOT)


def close_communication():
    logging.info("Closing robot TCP sockets...")

    _CANDY_SOCKET.close()
    _LEAFLET_SOCKET.close()


def request_prize(candy: int, category: str, ready_callback: Callable[[int], None]):
    if _EXECUTING_EVENT.is_set():
        logging.warning("Current candy request has not been finished, ignoring request!")
        return
    
    _EXECUTING_EVENT.set()
    result = RESPONSE_TIMEOUT  

    leaflet = int(list(categories.keys()).index(category))

    try:
        candy_command = str(candy)
        leaflet_command = str(leaflet)

        candy_result = False
        leaflet_result = False

        def run_candy():
            nonlocal candy_result
            candy_result = issue_command(_CANDY_SOCKET, IP_CANDY_ROBOT, PORT_CANDY_ROBOT, candy_command)

        def run_leaflet():
            nonlocal leaflet_result
            leaflet_result = issue_command(_LEAFLET_SOCKET, IP_LEAFLET_ROBOT, PORT_LEAFLET_ROBOT, leaflet_command)

        candy_thread = threading.Thread(target=run_candy, daemon=True)
        leaflet_thread = threading.Thread(target=run_leaflet, daemon=True)

        candy_thread.start()
        leaflet_thread.start()

        candy_thread.join()
        leaflet_thread.join()

        result = RESPONSE_SUCCESS if candy_result and leaflet_result else RESPONSE_TIMEOUT
        update_statistics(category)
    finally:
        _EXECUTING_EVENT.clear()

    ready_callback(result)


def issue_command(robot_socket: socket.socket, ip: str, port: int, command: str) -> bool:
    logging.info(f"Sending TCP command to {ip}:{port} = {command}")

    try:
        robot_socket.sendall(command.encode("utf-8"))
        response = robot_socket.recv(1024)
        if response:
            decoded_response = response.decode("utf-8").strip()
            logging.info(f"Received TCP response from {ip}:{port} = {decoded_response}")
            return True
        else:
            logging.warning("Received no TCP response")
    except socket.error as e:
        logging.error(
            f"No connection to TCP robot hand {ip}:{port}, attempting reconnect! Error: {e}"
        )

    return False

