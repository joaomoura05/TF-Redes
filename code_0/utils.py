import socket
import random
import time
import zlib
import os
import threading

# Constants
PACKET_SIZE = 10
TIMEOUT = 1  # Timeout for resending packets
LOSS_PROBABILITY = 0.1  # Probability of packet loss
CONGESTION_WINDOW_INITIAL = 1
CONGESTION_WINDOW_MAX = 16

# Helper functions
def calculate_crc(data):
    return zlib.crc32(data) & 0xffffffff

def introduce_error(data):
    if random.random() < LOSS_PROBABILITY:
        corrupted_data = bytearray(data)
        corrupted_data[random.randint(0, len(data)-1)] ^= 0xFF
        return bytes(corrupted_data)
    return data

def split_file(file_path):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(PACKET_SIZE)
            if not chunk:
                break
            yield chunk

def log(message):
    print(f"[LOG] {message}")