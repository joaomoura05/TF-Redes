from utils import *


def start(IP, PORT):
    # Cria um socket UDP
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((IP, PORT))
    print(f"Listening for UDP packets on {IP}:{PORT}")

    while True:
        # Recebe o dado do socket
        data, addr = server_sock.recvfrom(1024)

        # Aqui caso o dado = END termina a conexão
        if "END" in data.decode('utf-8'):
            print("Closing connection as requested by the client.")
            break
        else:
            process_packet(data, addr)


def process_packet(data, addr):
    print(f"Received packet from client {addr}: {data.decode('utf-8')}")


if __name__ == "__main__":
    start("0.0.0.0", 5005)
