from utils import *


def send_file(IP, PORT, data):
    global sequence_number
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.settimeout(1)
    cwnd = initial_cwnd

    try:
        i = 0
        while i < len(data):
            for j in range(cwnd):
                chunk_index = i + j * packet_size
                if chunk_index < len(data):
                    chunk = data[chunk_index:chunk_index + packet_size]
                    send_chunk(client_sock, IP, PORT, chunk, sequence_number)
                    sequence_number += 1
                else:
                    break
            i += cwnd * packet_size

            if cwnd < ssthresh:
                cwnd *= 2
            else:
                cwnd += 1

        print("File transmission completed")
        client_sock.sendto(b'END', (IP, PORT))

    finally:
        client_sock.close()

def send_chunk(client_sock, server_ip, server_port, chunk, sequence_number):
    chunk = chunk.ljust(packet_size, b'\0')  # Padding
    crc = calculate_crc(chunk)
    packet = sequence_number.to_bytes(4, 'big') + crc.to_bytes(4, 'big') + chunk
    packet = introduce_error(packet)

    while True:
        try:
            client_sock.sendto(packet, (server_ip, server_port))
            print(f"Sent packet {sequence_number}") # to {server_ip}:{server_port}")

            ack = client_sock.recv(1)
            ack_number = int.from_bytes(ack, 'big')
            print(f"ACK {ack_number}")

            if ack_number == sequence_number + 1:
                break
            else:
                print(f"Received out-of-order ACK {ack_number}")

        except socket.timeout:
            print("Timeout, resending packet")


        time.sleep(0.1)  # Add sleep to allow user to visualize message exchange

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()


if __name__ == "__main__":
    path = sys.argv[1]
    data = read_file(path)
    send_file("127.0.0.1", 5005, data)
