import ast

from dto.RisultatoDTO import RisultatoDTO
from flask import Flask
import logging
from flask_socketio import SocketIO
import json
from interfaces.Observable import Observable
from interfaces.Observator import Observator

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class SocketIOServer(Observable, Observator):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name=""):
        self.app = Flask(name)
        self.__observators = []
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self.socketio.on_event("connect", lambda data: self.__message_handler)
        self.socketio.on_event("message", self.__message_handler)

    def __on_connect(self, data):
        print(f'Someone is connected - {data}')

    def __message_handler(self, data):
        self.__notify_all_listeners(data)

    def send(self, event: str, body):
        self.__instance.socketio.emit(event, body)

    def start(self):
        self.__instance.socketio.run(self.__instance.app)

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)

    def on_notify(self, *args, **kwargs):
        data = ast.literal_eval(args[3].__str__())
        self.__instance.socketio.emit("message", data)
        logger.info(f'[on_notify] Invio {data}')

    def __notify_all_listeners(self, *args, **kwargs):
        for observator in self.__observators:
            observator.on_notify(*args, **kwargs)
