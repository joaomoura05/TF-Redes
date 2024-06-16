import socket
import hashlib

def log(message):
    print(message)

def calculate_crc(data):
    return sum(data) % 256

class UDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.expected_sequence_number = 0
        self.received_data = []
        self.received_packets = set()

    def start(self):
        log("Server started")
        while True:
            data, addr = self.sock.recvfrom(1024)
            if data == b'END':
                self.save_file()
                break
            self.process_packet(data, addr)

    def process_packet(self, packet, addr):
        sequence_number = int.from_bytes(packet[:4], 'big')
        crc_received = int.from_bytes(packet[4:8], 'big')
        data = packet[8:]
        crc_calculated = calculate_crc(data)

        if crc_received == crc_calculated:
            if sequence_number not in self.received_packets:
                self.received_packets.add(sequence_number)
                self.received_data.append(data)
                self.sock.sendto(sequence_number.to_bytes(4, 'big'), addr)
                log(f"Received and acknowledged packet {sequence_number}")
            else:
                log(f"Duplicate packet {sequence_number}, ignoring")
        else:
            log(f"Corrupted packet {sequence_number}, expected {self.expected_sequence_number}")

    def save_file(self):
        file_data = b''.join(self.received_data)
        with open('received_file', 'wb') as f:
            f.write(file_data)
        log("File saved as 'received_file'")

# Main program
if __name__ == '__main__':
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 12345

    server = UDPServer(SERVER_HOST, SERVER_PORT)
    server.start()