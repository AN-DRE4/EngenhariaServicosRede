import socket

def main():
    server_ip = input("Enter the server's IP address: ")
    server_port = 8888  # You can change the port if needed

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")

        while True:
            # send client's ip address to server
            message = socket.gethostbyname(socket.gethostname())
            client.send(message.encode())
            response = client.recv(1024)
            print(f"Server Response: {response.decode()}")

    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running and check the IP and port.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
