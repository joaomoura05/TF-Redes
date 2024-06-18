from utils import *


def send_file(IP, PORT, data):
    sequence_number = 0
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.settimeout(1) 
    cwnd = initial_cwnd  # Inicializa a janela de congestionamento
    ssthresh = 6  # Limiar de congestão

    try:
        i = 0
        while i < len(data):
            if cwnd < ssthresh:
                print("Slow start phase")
            else:
                print("Congestion avoidance phase")

            print(f"cwnd: {cwnd}")

            for j in range(int(cwnd)):
                chunk_index = i + j * packet_size
                if chunk_index < len(data):
                    chunk = data[chunk_index:chunk_index + packet_size]
                    send_chunk(client_sock, IP, PORT, chunk, sequence_number)
                    sequence_number += 1
                else:
                    break
            i += int(round(cwnd)) * packet_size

            if cwnd < ssthresh:
                cwnd *= 2  # Exponencialmente aumenta a janela
            else:
                cwnd += 1  # Linearmente aumenta a janela 

        print("File transmission completed")
        client_sock.sendto(b'END', (IP, PORT))  

    finally:
        client_sock.close()  

def send_chunk(client_sock, server_ip, server_port, chunk, sequence_number):
    # Preenche o chunk com zeros até o tamanho do pacote e calcula o CRC do chunk
    chunk = chunk.ljust(packet_size, b'\0')  
    crc = calculate_crc(chunk)  

    # Monta o pacote com número de sequência, CRC e dados
    packet = sequence_number.to_bytes(4, 'big') + crc.to_bytes(4, 'big') + chunk  
    packet = introduce_error(packet) 

    while True:
        try:
            # Envia o pacote para o servidor
            client_sock.sendto(packet, (server_ip, server_port))  
            print(f"Sent packet {sequence_number}")
            # Recebe ACK do servidor
            ack = client_sock.recv(1)  
            ack_number = int.from_bytes(ack, 'big')
            print(f"ACK {ack_number}")
  
            if ack_number == sequence_number + 1:
                break  
            else:
                print(f"Received out-of-order ACK {ack_number}")
                if ack_number < sequence_number + 1:
                    # Atualiza número de sequência se ACK for menor
                    sequence_number = ack_number  
                    break

        except socket.timeout:
            # Trata timeout, reenviando o pacote
            print(f"Timeout, resending packet {sequence_number}")  

        time.sleep(0.1)  


if __name__ == "__main__":
    path = sys.argv[1]
    if path == 'END':
        send_file("127.0.0.1", 5005, b'END')
    else:
        data = read_file(path)
        send_file("127.0.0.1", 5005, data)
