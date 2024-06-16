from utils import *


def send_file(IP, PORT, data):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 0

    try:
        # Aqui divide os dados em chunks e envia cada um com um número de sequência
        for i in range(0, len(data), packet_size):
            chunk = data[i:i + packet_size]
            send_chunk(client_sock, IP, PORT, chunk, sequence_number)
            # Incremente o número de sequência após cada envio
            sequence_number += 1

        # Termina a transmissão de dados
        print("File transmission completed")
        client_sock.sendto(b'END', (IP, PORT))

    finally:
        client_sock.close()


def send_chunk(client_sock, server_ip, server_port, chunk, sequence_number):
    # O código que você forneceu para enviar um chunk e esperar por um ACK
    # Simplesmente envia o chunk com o número de sequência (não implementado neste exemplo)
    chunk = chunk.encode('utf-8')
    chunk = chunk.ljust(packet_size, b'\0')  # Padding
    crc = calculate_crc(chunk)

    #packet = f"PACKET-{sequence_number}: CRC-{crc} : DATA-".encode('utf-8') + chunk
    packet = sequence_number.to_bytes(4, 'big') + crc.to_bytes(4, 'big') + chunk

    # packet = introduce_error(packet)

    while True:
        try:
            # Vai mandar o pacote para o servidor
            client_sock.sendto(packet, (server_ip, server_port))
            print(f"Sent packet {sequence_number} to {server_ip}:{server_port}")
            # Verificar
            ack = client_sock.recv(1)
            ack_number = int.from_bytes(ack, 'big')
            print('ACK', ack_number)

            if ack_number == sequence_number + 1:
                sequence_number += 1
                # self.adjust_congestion_window()
                break
            else:
                print(f"Received out-of-order ACK {ack_number}")

        except client_sock.timeout:
            print("Timeout, resending packet")
            # reset_congestion_window()


if __name__ == "__main__":
    path = sys.argv[1]
    if path == 'END':
        # Termina a transmissão de dados
        print("File transmission completed")
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_sock.sendto(b'END', ("127.0.0.1", 5005))
    else:
        data = read_file(path)
        send_file("127.0.0.1", 5005, data)
