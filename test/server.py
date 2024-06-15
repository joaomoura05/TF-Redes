import socket
import sys

def start(UDP_IP, UDP_PORT):
	# Create a UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))

	print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

	while True:
		# Receive data from the socket
		data, addr = sock.recvfrom(1024)
		print(f"Received packet from {addr}: {data.decode('utf-8')}")

if __name__ == "__main__":
	# Define the UDP IP address and port to listen on
	start("127.0.0.1", 5005, )
