import socket
import threading
import logging
from typing import Callable
from .question_bank import categories, update_statistics

CAMERA_CAPTURE: int = 0
PICKUP_CANDY: int = 1

RESPONSE_TIMEOUT: int = 0
RESPONSE_SUCCESS: int = 1
TCP_TIMEOUT_S: int = 30

IP_CANDY_ROBOT: str = "192.168.2.6"
PORT_CANDY_ROBOT: int = 6001
_CANDY_SOCKET: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_CANDY_SOCKET.settimeout(TCP_TIMEOUT_S)

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

def send_robot_command(robot_socket: socket.socket, ip: str, port: int, command: str) -> bool:
    """Sends a command to the specified robot and waits for a response."""
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

def send_candy_robot_command(x: float, y: float, z: float, r: float, todo: int) -> bool:
    """Sends a movement command to the candy robot."""
    command = f"{x},{y},{z},{r},{todo}"
    return send_robot_command(_CANDY_SOCKET, IP_CANDY_ROBOT, PORT_CANDY_ROBOT, command)


def send_leaflet_robot_command(category: str) -> bool:
    """Sends a command to the leaflet robot to dispense a leaflet for the given category."""
    leaflet_index = int(list(categories.keys()).index(category))
    return send_robot_command(_LEAFLET_SOCKET, IP_LEAFLET_ROBOT, PORT_LEAFLET_ROBOT, str(leaflet_index))



def request_prize(x: float, y: float, z: float, r: float, todo: int, category: str, ready_callback: Callable[[int], None]):
    if _EXECUTING_EVENT.is_set():
        logging.warning("Current candy request has not been finished, ignoring request!")
        return
    
    _EXECUTING_EVENT.set()
    result = RESPONSE_TIMEOUT  

    candy_result = False
    leaflet_result = False

    try:

        def run_candy():
            nonlocal candy_result
            candy_result = send_candy_robot_command(x, y, z, r, todo)

        def run_leaflet():
            nonlocal leaflet_result
            leaflet_result = send_leaflet_robot_command(category)

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