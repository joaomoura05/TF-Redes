import socket


def send_file(UDP_IP, UDP_PORT, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
		print(f"Sent UDP packet to {UDP_IP}:{UDP_PORT}: {message}")
	finally:
		sock.close()

# python client.py

if __name__ == "__main__":
	UDP_IP = "127.0.0.1"  # Replace with the target IP address
	UDP_PORT = 5005  # Replace with the target port
	message = "Opa"  # send the message via socket

	send_file(UDP_IP, UDP_PORT, message)