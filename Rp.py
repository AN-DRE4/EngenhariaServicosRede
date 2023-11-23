import socket
import threading
import json
from ServerWorker import ServerWorker

class Router:
    def __init__(self, name, ports):
        self.name = name
        self.SW = ServerWorker()