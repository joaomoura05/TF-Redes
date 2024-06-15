from utils import *

def send_file(UDP_IP, UDP_PORT, data):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
		print(f"Sent UDP packet to {UDP_IP}:{UDP_PORT}: {data}")
	finally:
		sock.close()

if __name__ == "__main__":

	path = sys.argv[1]

	if path == 'END':
		send_file("127.0.0.1", 5005, 'END')
	else:
		data = read_file(path)
		send_file("127.0.0.1", 5005, data)