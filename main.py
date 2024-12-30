import socket
import threading
import os
import time

# Terminal Effects
def matrix_effect():
    try:
        os.system("clear" if os.name == "posix" else "cls")
        print("\033[32m" + "Loading hacking terminal...\n")
        for _ in range(20):
            print("".join(chr(i) for i in range(33, 127)) * 2)
            time.sleep(0.05)
        os.system("clear")
    except KeyboardInterrupt:
        os.system("clear")

# Chat Server
def start_server(host="0.0.0.0", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"Server started on {host}:{port}. Waiting for connections...\n")
    except OSError as e:
        print(f"Error: {e}. Try using a different IP or port.")
        return

    clients = {}

    def handle_client(client_socket, addr):
        try:
            username = client_socket.recv(1024).decode("utf-8")
            clients[client_socket] = username
            broadcast(f"Server: {username} has joined the chat!", client_socket)
            print(f"{username} joined from {addr}")

            while True:
                message = client_socket.recv(1024).decode("utf-8")[:512]  # Limit message to 512 characters
                if message:
                    print(f"[{username}]: {message}")
                    broadcast(f"[{username}]: {message}", client_socket)
        except:
            username = clients.pop(client_socket, "Unknown")
            print(f"{username} disconnected.")
            broadcast(f"Server: {username} has left the chat.")
            client_socket.close()

    def broadcast(message, sender_socket=None):
        for client in list(clients.keys()):
            if client != sender_socket:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    client.close()
                    clients.pop(client, None)

    def send_host_messages():
        while True:
            host_message = input()
            broadcast(f"[Server Host]: {host_message}")

    threading.Thread(target=send_host_messages, daemon=True).start()

    while True:
        try:
            client_socket, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            for client in clients:
                client.close()
            server.close()
            break

# Chat Client
def start_client(server_ip="127.0.0.1", port=12345, username="Anonymous"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        client.send(username.encode("utf-8"))  # Send the username to the server
        print("Connected to the server. Type your messages below:\n")
    except Exception as e:
        print(f"Unable to connect to the server: {e}")
        return

    def receive_messages():
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message:
                    print(message)
            except:
                print("Disconnected from server.")
                client.close()
                break

    threading.Thread(target=receive_messages, daemon=True).start()

    while True:
        message = input()
        if message.lower() == "/exit":
            client.send(f"{username} has left the chat.".encode("utf-8"))
            client.close()
            break
        client.send(message.encode("utf-8"))

# Main Function
if __name__ == "__main__":
    matrix_effect()
    os.system("clear" if os.name == "posix" else "cls")

    print("Welcome to the Hacker Terminal!")
    print("1. Start Server")
    print("2. Connect to Server")
    choice = input("Choose an option: ")

    if choice == "1":
        host = input("Enter the IP address to host the server (default 0.0.0.0): ") or "0.0.0.0"
        port = int(input("Enter port to host the server on (default 12345): ") or 12345)
        start_server(host, port)
    elif choice == "2":
        server_ip = input("Enter server IP address (default 127.0.0.1): ") or "127.0.0.1"
        port = int(input("Enter server port (default 12345): ") or 12345)
        username = input("Enter your username: ")
        start_client(server_ip, port, username)
    else:
        print("Invalid option. Exiting.")
