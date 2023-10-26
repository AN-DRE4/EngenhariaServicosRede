import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8888))

    while True:
        message = input("Enter a message: ")
        client.send(message.encode())
        response = client.recv(1024)
        print(f"Server Response: {response.decode()}")

if __name__ == "__main__":
    main()
