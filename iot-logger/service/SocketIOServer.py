from flask import Flask
from flask_socketio import SocketIO


class SocketIOServer:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name=""):
        self.app = Flask(name)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

    def send(self, event: str, body):
        self.__instance.socketio.emit(event, body)

    def start(self):
        self.__instance.socketio.run(self.__instance.app)

