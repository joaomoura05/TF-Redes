import socket
import time
import os
import random
import hashlib

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
FILE_PATH = 'C:/Users/user/Documents/GitHub/TF-Redes/code_0/teste.txt'
TIMEOUT = 1
CONGESTION_WINDOW_INITIAL = 1
CONGESTION_WINDOW_MAX = 1000
PACKET_SIZE = 10  # Fixed packet size as per requirement

def log(message):
    print(message)

def split_file(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def calculate_crc(data):
    return sum(data) % 256

def introduce_error(packet):
    # Introduce errors with a probability of 10%
    if random.random() < 0.01:
        # In a real scenario, you might flip a bit or introduce a specific error
        log("Error introduced into packet")
        return b'ERROR' + packet  # Placeholder for error introduction
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
        self.expected_ack = 0
        self.received_acks = set()
        self.total_packets = 0

    def send_file(self):
        log("Starting file transmission")
        start_time = time.time()
        for chunk in split_file(self.file_path, PACKET_SIZE):
            self.send_chunk(chunk)
        self.end_transmission()
        end_time = time.time()
        log(f"Total transmission time: {end_time - start_time:.2f} seconds")

    def send_chunk(self, chunk):
        packet = self.sequence_number.to_bytes(4, 'big') + chunk
        packet = packet.ljust(PACKET_SIZE, b'\0')  # Padding to fixed packet size
        crc = calculate_crc(packet)
        packet = self.sequence_number.to_bytes(4, 'big') + crc.to_bytes(4, 'big') + chunk
        packet = introduce_error(packet)

        try_count = 0
        while try_count < 3:  # Attempt maximum of 3 retries on timeout
            try:
                if self.sequence_number not in self.sent_packets:
                    self.sock.sendto(packet, (self.server_ip, self.server_port))
                    self.sent_packets.add(self.sequence_number)
                    log(f"Sent packet {self.sequence_number}, CWND: {self.congestion_window}")

                ack_packet, addr = self.sock.recvfrom(1024)
                ack_number = int.from_bytes(ack_packet, 'big')

                if ack_number == self.sequence_number + 1:
                    self.received_acks.add(self.sequence_number)
                    self.sequence_number += 1
                    self.adjust_congestion_window()
                    log(f"Acknowledged packet {self.sequence_number}, CWND: {self.congestion_window}")
                    break
                else:
                    log(f"Received out-of-order ACK {ack_number}, CWND: {self.congestion_window}")
                    self.reset_congestion_window()

            except socket.timeout:
                try_count += 1
                log(f"Timeout {try_count}, resending packet")
                self.reset_congestion_window()
                packet = introduce_error(packet)

            except ConnectionResetError as e:
                log(f"Connection reset error: {e}")
                break  # Exit retry loop on connection reset

            except Exception as e:
                log(f"Unexpected error: {e}")
                break  # Exit retry loop on unexpected error
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

# Main program
if __name__ == '__main__':
    client = UDPClient(SERVER_IP, SERVER_PORT, FILE_PATH)
    client.send_file()