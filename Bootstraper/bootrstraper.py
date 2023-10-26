from icecream import ic
import socket
import threading

def read_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Strip trailing newline characters from each line and create a list of strings
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
def create_dict(lines):
    config_dict = {}
    for line in lines:
        # Split the line into key and value
        key, value = line.split(",")[0], line.split(",")[1:]
        # Strip leading and trailing whitespace from both key and value
        key = key.strip()
        # Add the key-value pair to the dictionary
        config_dict[key] = value
    return config_dict

def sendNeighbours(dic, client_ip):
    for key, value in dic.items():
        if key == client_ip:
            # make the value a string
            value = str(value)
            # remove the square brackets
            value = value.replace("[", "")
            value = value.replace("]", "")
            # remove the single quotes
            value = value.replace("'", "")
            return value

def handle_client(client_socket, dicionario):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        vizinhos = sendNeighbours(dicionario, client_socket.getpeername()[0])
        client_socket.send(vizinhos.encode())
    client_socket.close()

def connectToClient(dic):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))
    server.listen(5)
    print("Server listening on port 8888")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, dic,))
        client_handler.start()


def main():
    file_path = "config_file.txt"
    lines = read_file_to_list(file_path)
    dicionario = create_dict(lines)
    connectToClient(dicionario)


if __name__ == "__main__":
    main()
