import sys
import zlib
import random
import time
import socket


packet_size = 10
sequence_number = 0
expected_sequence_number = 0
received_data = []
initial_cwnd = 1
ssthresh = 64
loss_probability = 0.2 # Probability of loss


def read_file(path):
    with open(path, 'rb') as f:
        return f.read().rstrip()


def calculate_crc(data):
    return zlib.crc32(data) & 0xffffffff


def introduce_error(data):
    if random.random() < loss_probability:
        corrupted_data = bytearray(data)
        corrupted_data[random.randint(0, len(data)-1)] ^= 0xFF
        return bytes(corrupted_data)
    return data


def adjust_congestion_window():
    # Implemente a lógica para ajustar a janela de congestionamento
    pass


def reset_congestion_window():
    # Implemente a lógica para resetar a janela de congestionamento
    pass
