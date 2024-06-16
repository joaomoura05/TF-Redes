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
            process_packet(server_sock, data, addr)


def process_packet(server_sock, data, addr):
    global expected_sequence_number
    # print(f"Received packet from client {addr}: {data.decode('utf-8')}")
    info = re.match('PACKET-(\d+): CRC-(\d+) : DATA-([\w\s]*)', data.decode('utf-8'))

    sequence_number = int(info.group(1))
    crc_received = int(info.group(2))
    data = info.group(3)
    crc_calculated = calculate_crc(info.group(3).encode('utf-8'))

    if crc_received == crc_calculated:
        if sequence_number == expected_sequence_number:
            received_data.append(data.rstrip(b'\0'))
            expected_sequence_number += 1
            server_sock.sendto(bytes([expected_sequence_number]), addr)
            # print(data)
            print(f"Received and ACK packet {sequence_number}")
        else:
            print(f"Out-of-order packet {sequence_number}, expected {expected_sequence_number}")
            server_sock.sendto(bytes([expected_sequence_number]), addr)
    else:
        # print(data)
        # print(crc_received, crc_calculated)
        # print(type(crc_received), type(crc_calculated))
        print(f"Corrupted packet {sequence_number}, expected {expected_sequence_number}")


if __name__ == "__main__":
    start("0.0.0.0", 5005)
