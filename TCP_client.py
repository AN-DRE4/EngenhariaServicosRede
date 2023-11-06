import os
os.environ['DISPLAY'] = ':0'

import socket
import cv2
import numpy as np

def main():
    server_ip = input("Enter the server's IP address: ")
    server_port = 8888  # You can change the port if needed

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")

        cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)

        while True:
            # Receive the size of the frame
            frame_size = int(client.recv(16))
            if frame_size == 0:
                break

            # Receive the frame data
            frame_data = b''
            while len(frame_data) < frame_size:
                data = client.recv(frame_size - len(frame_data))
                if not data:
                    break
                frame_data += data

            if len(frame_data) < frame_size:
                break

            # Decode the frame and display it
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow("Video Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        client.close()
        cv2.destroyAllWindows()

    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running and check the IP and port.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
