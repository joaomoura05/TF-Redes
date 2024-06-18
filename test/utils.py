# Importa módulos necessários
import sys  
import zlib  
import random  
import time  
import socket  

# Define constantes e variáveis globais
packet_size = 10  
sequence_number = 0  
expected_sequence_number = 0  
received_data = []  
initial_cwnd = 1  
ssthresh = 64  
loss_probability = 0.0  

# Função para ler um arquivo e retornar seu conteúdo em bytes (removendo espaços em branco no final)
def read_file(path):
    with open(path, 'rb') as f:
        return f.read().rstrip()

# Função para calcular o CRC (Cyclic Redundancy Check) dos dados
def calculate_crc(data):
    return zlib.crc32(data) & 0xffffffff

# Função para introduzir erros aleatórios nos dados (simulação de perda de pacotes)
def introduce_error(data):
    if random.random() < loss_probability:
        corrupted_data = bytearray(data)
        corrupted_data[random.randint(0, len(data)-1)] ^= 0xFF
        return bytes(corrupted_data)
    return data

# Função para ajustar a janela de congestionamento (não implementada)
def adjust_congestion_window():
    # Implemente a lógica para ajustar a janela de congestionamento
    pass

# Função para resetar a janela de congestionamento (não implementada)
def reset_congestion_window():
    # Implemente a lógica para resetar a janela de congestionamento
    pass
