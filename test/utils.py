import sys
import socket

def read_file(path):
	try:
		with open(path, 'r') as p:
			data = p.read().rstrip()
			return data
	except FileNotFoundError:
		print(f"Path '{path}' not found.")
		sys.exit(1)