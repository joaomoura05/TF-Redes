# Importa funções e constantes necessárias do módulo utils
from utils import *

# Define a classe UDPServer
class UDPServer:
    # Inicializa o servidor UDP com host e porta
    def __init__(self, host, port):  # Corrige a inicialização (de _init_ para __init__)
        self.host = host  # Host do servidor
        self.port = port  # Porta do servidor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
        self.sock.bind((self.host, self.port))  # Faz o bind do socket ao host e porta
        self.expected_sequence_number = 0  # Número de sequência esperado inicialmente
        self.received_data = []  # Lista para armazenar os dados recebidos

    # Inicia o servidor UDP
    def start(self):
        log("Server started")  # Registra o início do servidor
        while True:
            data, addr = self.sock.recvfrom(1024)  # Recebe dados do cliente
            if data == b'END':  # Se receber a mensagem de término
                self.save_file()  # Salva o arquivo
                break  # Encerra o loop
            self.process_packet(data, addr)  # Processa o pacote recebido

    # Processa um pacote recebido
    def process_packet(self, packet, addr):
        sequence_number = int.from_bytes(packet[:4], 'big')  # Extrai o número de sequência
        crc_received = int.from_bytes(packet[4:8], 'big')  # Extrai o CRC recebido
        data = packet[8:]  # Extrai os dados
        crc_calculated = calculate_crc(data)  # Calcula o CRC dos dados

        if crc_received == crc_calculated:  # Verifica a integridade dos dados
            if sequence_number == self.expected_sequence_number:  # Se o número de sequência for o esperado
                self.received_data.append(data.rstrip(b'\0'))  # Adiciona os dados recebidos (removendo padding)
                self.expected_sequence_number += 1  # Incrementa o número de sequência esperado
                self.sock.sendto(self.expected_sequence_number.to_bytes(4, 'big'), addr)  # Envia ACK
                log(f"Received and acknowledged packet {sequence_number}")  # Registra o recebimento e ACK do pacote
            else:
                log(f"Out-of-order packet {sequence_number}, expected {self.expected_sequence_number}")  # Registra pacote fora de ordem
                self.sock.sendto(self.expected_sequence_number.to_bytes(4, 'big'), addr)  # Reenvia o ACK esperado
        else:
            log(f"Corrupted packet {sequence_number}, expected {self.expected_sequence_number}")  # Registra pacote corrompido

    # Salva os dados recebidos em um arquivo
    def save_file(self):
        file_data = b''.join(self.received_data)  # Junta todos os dados recebidos
        with open('received_file', 'wb') as f:  # Abre um arquivo para escrita em modo binário
            f.write(file_data)  # Escreve os dados no arquivo
        log("File saved as 'received_file'")  # Registra que o arquivo foi salvo

# Uso do servidor UDP
server = UDPServer('0.0.0.0', 12345)  # Cria uma instância do servidor UDP
server.start()  # Inicia o servidor