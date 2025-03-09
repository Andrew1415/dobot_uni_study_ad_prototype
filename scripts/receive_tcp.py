import socket
import argparse

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((ip, port))
        server_socket.listen(5)
        print(f"Server listening on {ip}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    print("Empty message received, closing connection.")
                    client_socket.close()
                    continue
                
                print(f"Received: {data}")
            except socket.error as e:
                print(f"Error handling client {client_address}: {e}")
    except socket.error as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP server that echoes received messages.")
    parser.add_argument("ip", help="The IP address to bind the server to.")
    parser.add_argument("port", type=int, help="The port number to listen on.")
    
    args = parser.parse_args()
    start_server(args.ip, args.port)
