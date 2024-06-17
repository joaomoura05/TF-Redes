# Importa funções e constantes necessárias do módulo utils
from utils import *

# Define a classe UDPClient
class UDPClient:
    # Inicializa o cliente UDP com IP do servidor, porta do servidor e caminho do arquivo
    def __init__(self, server_ip, server_port, file_path):  # Corrige a inicialização (de _init_ para __init__)
        self.server_ip = server_ip  # IP do servidor
        self.server_port = server_port  # Porta do servidor
        self.file_path = file_path  # Caminho do arquivo a ser enviado
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
        self.sock.settimeout(TIMEOUT)  # Define o tempo de espera para o socket
        self.sequence_number = 0  # Número de sequência inicial
        self.congestion_window = CONGESTION_WINDOW_INITIAL  # Tamanho inicial da janela de congestionamento
        self.ssthresh = CONGESTION_WINDOW_MAX  # Limite da janela de congestionamento (slow start threshold)

    # Envia o arquivo para o servidor
    def send_file(self):
        log("Starting file transmission")  # Registra o início da transmissão do arquivo
        for chunk in split_file(self.file_path):  # Divide o arquivo em partes (chunks)
            self.send_chunk(chunk)  # Envia cada parte do arquivo
        self.end_transmission()  # Finaliza a transmissão

    # Envia um pedaço (chunk) do arquivo
    def send_chunk(self, chunk):
        chunk = chunk.ljust(PACKET_SIZE, b'\0')  # Adiciona padding ao chunk para garantir o tamanho do pacote
        crc = calculate_crc(chunk)  # Calcula o CRC do chunk para verificação de integridade
        # Cria o pacote com número de sequência, CRC e o chunk de dados
        packet = self.sequence_number.to_bytes(4, 'big') + crc.to_bytes(4, 'big') + chunk
        packet = introduce_error(packet)  # Introduz erros no pacote para testes (opcional)

        while True:
            try:
                # Envia o pacote para o servidor
                self.sock.sendto(packet, (self.server_ip, self.server_port))
                log(f"Sent packet {self.sequence_number}")  # Registra o envio do pacote
                ack = self.sock.recv(4)  # Aguarda recebimento do ACK
                ack_number = int.from_bytes(ack, 'big')  # Converte ACK de bytes para inteiro
                if ack_number == self.sequence_number + 1:  # Verifica se o ACK é o esperado
                    self.sequence_number += 1  # Incrementa o número de sequência
                    self.adjust_congestion_window()  # Ajusta a janela de congestionamento
                    break
                else:
                    log(f"Received out-of-order ACK {ack_number}")  # Registra ACK fora de ordem
            except socket.timeout:  # Em caso de timeout
                log("Timeout, resending packet")  # Registra o timeout e tenta reenviar o pacote
                self.reset_congestion_window()  # Reseta a janela de congestionamento

    # Ajusta a janela de congestionamento
    def adjust_congestion_window(self):
        if self.congestion_window < self.ssthresh:  # Se a janela de congestionamento está abaixo do limite
            self.congestion_window *= 2  # Multiplica por 2 (fase de slow start)
        else:
            self.congestion_window += 1  # Incrementa de 1 (fase de congestion avoidance)
        log(f"Adjusted congestion window to {self.congestion_window}")  # Registra o ajuste da janela

    # Reseta a janela de congestionamento
    def reset_congestion_window(self):
        self.ssthresh = max(self.congestion_window // 2, 1)  # Ajusta o limite da janela para metade do tamanho atual
        self.congestion_window = CONGESTION_WINDOW_INITIAL  # Reseta a janela de congestionamento para o valor inicial
        log(f"Reset congestion window to {self.congestion_window}")  # Registra o reset da janela

    # Finaliza a transmissão do arquivo
    def end_transmission(self):
        log("File transmission completed")  # Registra o término da transmissão do arquivo
        self.sock.sendto(b'END', (self.server_ip, self.server_port))  # Envia um pacote de término para o servidor

# Uso do cliente UDP
client = UDPClient('127.0.0.1', 12345, 'test_file.txt')  # Cria uma instância do cliente UDP
client.send_file()  # Inicia a transmissão do arquivo
