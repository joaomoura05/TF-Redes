from utils import * 
import socket
import time

def process_packet(server_sock, data, addr, expected_sequence_number, received_data):
    # Extrai o número de sequência do pacote, CRC e data
    sequence_number = int.from_bytes(data[:4], 'big')
    crc_received = int.from_bytes(data[4:8], 'big')
    data = data[8:]  
    crc_calculated = calculate_crc(data)  # Calcula o CRC 

    print(f"Received packet {sequence_number} from {addr}")

    # Verifica se o pacote está corrompido comparando CRCs
    if crc_received == crc_calculated:
        # Verifica se o número de sequência está correto
        if sequence_number == expected_sequence_number:
            received_data.append(data.rstrip(b'\0'))  
            expected_sequence_number += 1  
            server_sock.sendto(bytes([expected_sequence_number]), addr)  # Envia ACK para o cliente
            print(f"Packet {sequence_number} received correctly. Sending ACK {expected_sequence_number}")
        else:
            print(f"Out-of-order packet {sequence_number}, expected {expected_sequence_number}")
            server_sock.sendto(bytes([expected_sequence_number]), addr)  
    else:
        # Se o pacote estiver corrompido
        print(f"Corrupted packet {sequence_number}, expected {expected_sequence_number}")
        server_sock.sendto(bytes([expected_sequence_number]), addr)  

    time.sleep(0.5)  
    return expected_sequence_number, received_data

def start(IP, PORT):
    # Configura o socket UDP e faz o bind para o IP e porta especificados
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((IP, PORT))
    print(f"Listening for UDP packets on {IP}:{PORT}")

    expected_sequence_number = 0  
    received_data = []  

    while True:
        # Recebe dados do cliente e o endereço do cliente
        data, addr = server_sock.recvfrom(1024)
        
        # Fim da conexão
        if data == b'END':
            print("Closing connection as requested by the client.")
            break
        else:
            # Processa o pacote recebido
            expected_sequence_number, received_data = process_packet(server_sock, data, addr, expected_sequence_number, received_data)

    # Após receber todos os dados, escreve os dados recebidos em um arquivo 'received_file.txt'
    with open('received_file.txt', 'wb') as f:
        for chunk in received_data:
            f.write(chunk)
    print("File received and saved as 'received_file.txt'.")

if __name__ == "__main__":
    start("0.0.0.0", 5005)  # Inicia o servidor na interface 0.0.0.0 e porta 5005
