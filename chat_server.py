import socket
import threading
import datetime

HOST = '0.0.0.0'
PORT = 5000
clients = []
log_file = "chat_log.txt"

def log_message(message):
    with open(log_file, "a") as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {message}\n")

def broadcast(message, sender_socket=None):
    log_message(message)
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    name = client_socket.recv(1024).decode()
    welcome_msg = f"{name} has joined the chat."
    broadcast(welcome_msg)

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg == "/exit":
                goodbye = f"{name} has left the chat."
                broadcast(goodbye, client_socket)
                clients.remove(client_socket)
                client_socket.close()
                break
            broadcast(f"{name}: {msg}", client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Server] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"[Connection] {addr} connected.")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
