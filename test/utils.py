import sys
import socket
import zlib
import random


packet_size = 10
loss_probability = 0.1  # Probability of packet loss


def read_file(path):
    try:
        with open(path, 'r') as p:
            data = p.read().rstrip()
            return data
    except FileNotFoundError:
        print(f"Path '{path}' not found.")
        sys.exit(1)


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
