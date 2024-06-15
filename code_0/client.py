import socket

# Placeholder constants
TIMEOUT = 1
CONGESTION_WINDOW_INITIAL = 1
CONGESTION_WINDOW_MAX = 1000
PACKET_SIZE = 1024

def log(message):
    # Placeholder for the logging function
    print(message)

def split_file(file_path):
    # Placeholder for the file splitting function
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(PACKET_SIZE - 8)  # Adjust size for headers
            if not chunk:
                break
            yield chunk

def calculate_crc(data):
    # Placeholder for the CRC calculation function
    return sum(data) % 256  # Example CRC calculation

def introduce_error(packet):
    # Placeholder for the function to introduce error
    return packet

class UDPClient:
    def __init__(self, server_ip, server_port, file_path):
        self.server_ip = server_ip
        self.server_port = server_port
        self.file_path = file_path
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT)
        self.sequence_number = 0
        self.congestion_window = CONGESTION_WINDOW_INITIAL
        self.ssthresh = CONGESTION_WINDOW_MAX

    def send_file(self):
        log("Starting file transmission")
        for chunk in split_file(self.file_path):
            self.send_chunk(chunk)
        self.end_transmission()

    def send_chunk(self, chunk):
        chunk = chunk.ljust(PACKET_SIZE - 8, b'\0')  # Padding
        crc = calculate_crc(chunk)
        packet = self.sequence_number.to_bytes(4, 'big') + crc.to_bytes(4, 'big') + chunk
        packet = introduce_error(packet)

        while True:
            try:
                self.sock.sendto(packet, (self.server_ip, self.server_port))
                log(f"Sent packet {self.sequence_number}")
                ack = self.sock.recv(4)
                ack_number = int.from_bytes(ack, 'big')
                if ack_number == self.sequence_number + 1:
                    self.sequence_number += 1
                    self.adjust_congestion_window()
                    break
                else:
                    log(f"Received out-of-order ACK {ack_number}")
            except socket.timeout:
                log("Timeout, resending packet")
                self.reset_congestion_window()

    def adjust_congestion_window(self):
        if self.congestion_window < self.ssthresh:
            self.congestion_window *= 2
        else:
            self.congestion_window += 1
        log(f"Adjusted congestion window to {self.congestion_window}")

    def reset_congestion_window(self):
        self.ssthresh = max(self.congestion_window // 2, 1)
        self.congestion_window = CONGESTION_WINDOW_INITIAL
        log(f"Reset congestion window to {self.congestion_window}")

    def end_transmission(self):
        log("File transmission completed")
        self.sock.sendto(b'END', (self.server_ip, self.server_port))

# Usage
client = UDPClient('127.0.0.1', 12345, 'C:/Users/user/Documents/GitHub/TF-Redes/code_0/teste.txt')
client.send_file()
