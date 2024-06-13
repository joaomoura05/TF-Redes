from utils import *

# Start server in a separate thread
server_thread = threading.Thread(target=lambda: server.start())
server_thread.start()

# Start client
client.send_file()