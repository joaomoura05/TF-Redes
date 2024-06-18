# Importa módulos necessários
import socket
import random
import time
import zlib
import os
import threading

# Constantes
PACKET_SIZE = 10  # Tamanho do pacote em bytes
TIMEOUT = 1  # Tempo de espera para reenvio de pacotes (em segundos)
LOSS_PROBABILITY = 0.1  # Probabilidade de perda de pacotes (10%)
CONGESTION_WINDOW_INITIAL = 1  # Tamanho inicial da janela de congestionamento
CONGESTION_WINDOW_MAX = 16  # Tamanho máximo da janela de congestionamento

# Funções auxiliares

# Calcula o CRC (Cyclic Redundancy Check) dos dados para verificação de integridade
def calculate_crc(data):
    return zlib.crc32(data) & 0xffffffff  # Retorna o CRC calculado dos dados

# Introduz erro nos dados com base na probabilidade de perda de pacotes
def introduce_error(data):
    if random.random() < LOSS_PROBABILITY:  # Se o número aleatório for menor que a probabilidade de perda
        corrupted_data = bytearray(data)  # Converte os dados para um bytearray (mutável)
        corrupted_data[random.randint(0, len(data)-1)] ^= 0xFF  # Introduz um erro aleatório nos dados
        return bytes(corrupted_data)  # Retorna os dados corrompidos como bytes
    return data  # Se não houver perda, retorna os dados originais

# Divide um arquivo em pedaços (chunks) de tamanho fixo
def split_file(file_path):
    with open(file_path, 'rb') as f:  # Abre o arquivo em modo binário de leitura
        while True:
            chunk = f.read(PACKET_SIZE)  # Lê um pedaço do arquivo do tamanho do pacote
            if not chunk:  # Se não houver mais dados para ler
                break  # Encerra o loop
            yield chunk  # Gera o pedaço lido

# Função para registrar mensagens de log
def log(message):
    print(f"[LOG] {message}")  # Imprime a mensagem de log com um prefixo [LOG]