import socket
import threading
import cv2
import numpy as np

def handle_client(client_socket, video_path):
    cap = cv2.VideoCapture(video_path)  # Replace with your video file path

    while True:  # Loop to restart the video when it's over
        while True:
            ret, frame = cap.read()

            if not ret:
                break  # If the video is over, break the inner loop

            _, encoded_frame = cv2.imencode(".jpg", frame)
            data = np.array(encoded_frame).tobytes()
           # Only encode and send the frame if it's not empty
            if frame is not None and frame.size > 0:
                _, encoded_frame = cv2.imencode(".jpg", frame)
                data = np.array(encoded_frame).tobytes()
                client_socket.send(str(len(data)).ljust(16).encode('utf-8'))
                client_socket.send(data)

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset the video to the first frame


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))
    server.listen(5)
    video_path = input("Enter the path to the video file: ")
    print("Server listening on port 8888")
    

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,video_path))
        client_handler.start()

if __name__ == "__main__":
    main()