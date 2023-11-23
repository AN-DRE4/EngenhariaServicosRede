from icecream import ic
import sys
import socket
import threading
import json

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
    
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data
    
def create_dict(data):
    config_dict = {}
    config_dict["Rp"] = list(data.values())[0]
    config_dict["type"] = list(data.values())[2]
    config_dict["port_tcp"] = 5000
    config_dict["port_udp"] = 6000
    '''for line in lines:
        # Split the line into key and value
        key, value = line.split(",")[0], line.split(",")[1:]
        # Strip leading and trailing whitespace from both key and value
        key = key.strip()
        # Add the key-value pair to the dictionary
        config_dict[key] = value'''
    config_dict["neighbors"] = list(data.values())[1]
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
    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    print("Server listening on port 5000")

    while True:
        client_socket, addr = server.accept()
        dic["ip"] = addr
        ic(dic)
        '''message = client_socket.recv(1024).decode()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, dic))
        client_handler.start()'''


def main():
    file_path = sys.argv[1]
    data = read_json_file(file_path)
    dicionario = create_dict(data)
    connectToClient(dicionario)


if __name__ == "__main__":
    main()
