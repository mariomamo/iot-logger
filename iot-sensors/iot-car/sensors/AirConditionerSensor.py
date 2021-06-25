import datetime
import logging

from dto.PayloadDTO import PayloadDTO
from dto.ResponseMessageDTO import ResponseMessageDTO
from interfaces.Observable import Observable
from interfaces.Observator import Observator

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class AirConditionerSensor(Observator, Observable):
    def __init__(self, sensorType, chatId, name, image, send_topic_name):
        self.__sensorType = sensorType
        self.__send_topic_name = send_topic_name
        self.__chatId = chatId
        self.__name = name
        self.__image = image
        self.__headers = {'Content-Type': 'application/json'}
        self.__observators = []
        self.__status = 20

    @property
    def chatId(self):
        return self.__chatId

    @chatId.setter
    def chatId(self, value):
        pass

    def on_notify(self, *args, **kwargs):
        message = args[0]
        if message == "subscribed":
            logger.info("A new subsriber is connected")
        elif message == "message":
            body = args[4]

            message = "I'm sorry, i'm not understand your command"
            now = datetime.datetime.now()
            payload = PayloadDTO(f'{now.hour}:{now.minute}', "text", message)

            if body['payload']['message'].lower() == 'set 20°':
                message = "Temperature setted to 20°"
                self.__status = 20
            elif body['payload']['message'].lower() == 'set 22°':
                message = "Temperature setted to 22°"
                self.__status = 22
            elif body['payload']['message'].lower() == 'set 24°':
                message = "Temperature setted to 24°"
                self.__status = 24
            elif body['payload']['message'].lower() == 'set 26°':
                message = "Temperature setted to 26°"
                self.__status = 26
            elif body['payload']['message'].lower() == 'set 28°':
                message = "Temperature setted to 28°"
                self.__status = 28
            elif body['payload']['message'].lower() == 'set 30°':
                message = "Temperature setted to 30°"
                self.__status = 30
            elif body['payload']['message'].lower() == 'status':
                message = f"The temperature is {self.__status}°"

            payload.message = message

            responseMessage = ResponseMessageDTO(self.__sensorType, self.__chatId, self.__name, self.__image, payload)

            logger.info(f"Invio {responseMessage}")

            self.__notify_all_listeners("message", responseMessage)

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)
        self.__notify_all_listeners("subscribed", self.__sensorType, self.__send_topic_name, self.__chatId,
                                    self.__image, "I'm connected")

    def __notify_all_listeners(self, message, *args, **kwargs):
        logger.info(f'Notify all {self.__observators.__len__()} listeners')
        for observator in self.__observators:
            observator.on_notify(message, *args, **kwargs)
