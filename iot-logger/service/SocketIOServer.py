import ast
import logging

import waitress
from flask import Flask, request, session
from flask_socketio import SocketIO, join_room, send

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
        self.__connectedDevices = {}
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self.socketio.on_event("message", self.__message_handler)
        self.socketio.on_event("join", self.__on_join)

    def __on_join(self, sid):
        logger.info(f'{sid} joined')
        join_room(sid)
        for device in self.__connectedDevices.values():
            logger.info(f'Send device info {device}')
            self.__instance.socketio.emit("message", device, room=sid)

    def __message_handler(self, data):
        logger.info(f'Recevied {data}')
        self.__notify_all_listeners(data)

    def send(self, event: str, body):
        chatId = body['data']['chatId']
        if chatId not in self.__connectedDevices:
            self.__connectedDevices[chatId] = body
        room = body['data']['userId']
        logger.info(f'Invio {body} sulla room {room}')

        self.__instance.socketio.emit(event, body, room=room)

    def start(self, host_ip="", port=5000):
        logger.info(f'[SOCKET IO SERVER RUNNIG] Server running on host {host_ip} and port {port}')
        self.app.app_context().push()
        waitress.serve(self.app, listen=f'{host_ip}:{port}')

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)

    def on_notify(self, *args, **kwargs):
        data = ast.literal_eval(args[3].__str__())
        logger.info(f'[on_notify] Invio {data}')
        self.__instance.socketio.emit("message", data)

    def __notify_all_listeners(self, *args, **kwargs):
        for observator in self.__observators:
            observator.on_notify(*args, **kwargs)
