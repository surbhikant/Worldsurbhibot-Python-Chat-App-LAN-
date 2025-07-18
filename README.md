@@ -1,2 +1,234 @@
# Python-Chat-App-LAN-
This Python LAN Chat Application is a simple yet powerful real-time messaging system designed for users on the same local network (LAN). It enables multiple users to communicate instantly through a graphical chat interface.
# 📁 PYTHON CHAT APP 
- This Python LAN Chat Application is a simple yet powerful real-time messaging system designed for users on the same local network (LAN). It enables multiple users to communicate instantly through a graphical chat interface.

# ✅ Features Included :-

# 1. Real-Time Chat:
 - Instant messaging between multiple clients connected to the same LAN.
 - Users can send and receive messages instantly over a Local Area Network without needing an internet connection.
 - All clients connected to the server receive messages in real time.

# 2. Multi-Client Support: 
 - Server can handle several users simultaneously using threading.
 - The server supports multiple users simultaneously using Python’s threading module.
 - Each connected client runs on a separate thread, ensuring smooth and uninterrupted communication for all users.

# 3. GUI chat window (Tkinter).
 - Each client uses a graphical interface built with Tkinter, providing an easy-to-use chat window with input and message display areas.
 - This enhances usability compared to a text-only interface.

# 4. Join/Leave Notifications: 
 - Alerts all users when someone enters or exits the chat.
 - The server broadcasts notifications when a user joins or leaves the chat, helping everyone stay informed about active participants.

# 5. Chat logs saved to a file.
 - Server records all messages with timestamps in a chat_log.txt file.
 - This allows for future review of conversations and adds a level of accountability.

# 6. Chat command:
 - The app includes basic slash commands for better control and user experience:

🔹 /exit – Allows a user to leave the chat and close their client window safely.
 
🔹 /mute – Temporarily mutes incoming messages for the user, useful in situations where the user needs silence without disconnecting.

🚀 This project is ideal for beginners learning about socket programming, GUI development, and multi-threading in Python. It's perfect for small group communication in classrooms, local office networks, or home setups.

# Technologies Used:

1. PYTHON
2. SOCKET
3. THREADING
4. Tkinter

# 🖥 1. Server Code (chat_server.py)

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

if _name_ == "_main_":

    start_server()



# 💬 2. Client Code (chat_client.py)

import socket

import threading

import tkinter as tk

from tkinter import scrolledtext, simpledialog, messagebox

HOST = '127.0.0.1'  # Change to server IP

PORT = 5000

class ChatClient:

    def _init_(self, master):
        self.master = master
        self.master.title("LAN Chat")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.muted = False

        self.chat_window = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_window.pack(padx=10, pady=10)

        self.entry = tk.Entry(master)
        self.entry.pack(fill='x', padx=10)
        self.entry.bind("<Return>", self.send_message)

        self.name = simpledialog.askstring("Name", "Enter your name:")
        if not self.name:
            self.master.destroy()
            return

        try:
            self.socket.connect((HOST, PORT))
            self.socket.send(self.name.encode())
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")
            self.master.destroy()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        if msg == "/exit":
            self.socket.send(msg.encode())
            self.master.destroy()
        elif msg == "/mute":
            self.muted = not self.muted
            self.append_message("[Muted]" if self.muted else "[Unmuted]")
        else:
            self.socket.send(msg.encode())
        self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                msg = self.socket.recv(1024).decode()
                if not self.muted:
                    self.append_message(msg)
            except:
                break

    def append_message(self, msg):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, msg + "\n")
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')

if _name_ == "_main_":

    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()


# 🧪 Testing :-
# 💡Terminal 1 (Server):
- Open a new terminal in VS Code: Terminal → New Terminal.
- Run the server:

       python chat_server.py

- You should see:
  
       [Server] Listening on 0.0.0.0:5000

# 💡Terminal 2 (Clients):
- Open another terminal in VS Code.
- Run the client:
  
       python chat_client.py

- Enter your name when prompted.
- A chat window will open.



# 📁LOGS
 - Logs are saved to "chat_log.txt" on the server with timestamps.


# 💡 Next Steps / Ideas
- Add timestamps in client UI.
- GUI for showing online users.
- Private messages using

           /pm <user> <message>.


# ✨ Author

SURBHI KANT
