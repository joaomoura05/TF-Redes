from utils import *
import socket

def process_packet(server_sock, data, addr, expected_sequence_number, received_data):
    sequence_number = int.from_bytes(data[:4], 'big')
    crc_received = int.from_bytes(data[4:8], 'big')
    data = data[8:]
    crc_calculated = calculate_crc(data)

    print(f"Received packet {sequence_number} from {addr}")

    if crc_received == crc_calculated:
        if sequence_number == expected_sequence_number:
            received_data.append(data.rstrip(b'\0'))
            expected_sequence_number += 1
            server_sock.sendto(bytes([expected_sequence_number]), addr)
            print(f"Received and ACK packet {sequence_number}")
        else:
            print(f"Out-of-order packet {sequence_number}, expected {expected_sequence_number}")
            server_sock.sendto(bytes([expected_sequence_number]), addr)
    else:
        print(f"Corrupted packet {sequence_number}, expected {expected_sequence_number}")
        server_sock.sendto(bytes([expected_sequence_number]), addr)

    time.sleep(0.1)
    return expected_sequence_number, received_data

def start(IP, PORT):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((IP, PORT))
    print(f"Listening for UDP packets on {IP}:{PORT}")

    expected_sequence_number = 0
    received_data = []

    while True:
        data, addr = server_sock.recvfrom(1024)
        if data == b'END':
            print("Closing connection as requested by the client.")
            break
        else:
            expected_sequence_number, received_data = process_packet(server_sock, data, addr, expected_sequence_number, received_data)

    with open('received_file.txt', 'wb') as f:
        for chunk in received_data:
            f.write(chunk)
    print("File received and saved as 'received_file.txt'.")

if __name__ == "__main__":
    start("0.0.0.0", 5005)