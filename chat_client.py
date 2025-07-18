import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = '127.0.0.1'  # Change to server IP
PORT = 5000

class ChatClient:
    def __init__(self, master):
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

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
