class UDPServer:
    def _init_(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.expected_sequence_number = 0
        self.received_data = []

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
            if sequence_number == self.expected_sequence_number:
                self.received_data.append(data.rstrip(b'\0'))
                self.expected_sequence_number += 1
                self.sock.sendto(self.expected_sequence_number.to_bytes(4, 'big'), addr)
                log(f"Received and acknowledged packet {sequence_number}")
            else:
                log(f"Out-of-order packet {sequence_number}, expected {self.expected_sequence_number}")
                self.sock.sendto(self.expected_sequence_number.to_bytes(4, 'big'), addr)
        else:
            log(f"Corrupted packet {sequence_number}, expected {self.expected_sequence_number}")

    def save_file(self):
        file_data = b''.join(self.received_data)
        with open('received_file', 'wb') as f:
            f.write(file_data)
        log("File saved as 'received_file'")


# Usage
server = UDPServer('0.0.0.0', 12345)
server.start()