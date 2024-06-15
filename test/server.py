from utils import *

def start(UDP_IP, UDP_PORT):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

    while True:
        # Receive data from the socket
        data, addr = sock.recvfrom(1024)
        print(f"Received packet from client {addr}: {data.decode('utf-8')}")

        # Check if the received data contains "END"
        if "END" in data.decode('utf-8'):
            print("Closing connection as requested by the client.")
            break  # Exit the loop and close the connection


def receive_data(sock):
    while True:
        # Receive data from the socket
        data, addr = sock.recvfrom(1024)
        print(f"Received packet from client {addr}: {data.decode('utf-8')}")

        # END CONNECTION
        # Check if the received data contains "END"
        if "END" in data.decode('utf-8'):
            print("Closing connection as requested by the client.")
            break


if __name__ == "__main__":
    start("0.0.0.0", 5005)
