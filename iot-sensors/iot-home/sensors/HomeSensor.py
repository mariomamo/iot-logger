import logging

from dto.PayloadDTO import PayloadDTO
from dto.ResponseMessageDTO import ResponseMessageDTO
from interfaces.Observable import Observable
from interfaces.Observator import Observator

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class CarSensor(Observator, Observable):
    def __init__(self, sensorType, chatId, name, image):
        self.__sensorType = sensorType
        self.__chatId = chatId
        self.__name = name
        self.__image = image
        self.__headers = {'Content-Type': 'application/json'}
        self.__observators = []

    @property
    def chatId(self):
        return self.__chatId

    @chatId.setter
    def chatId(self, value):
        pass

    def on_notify(self, *args, **kwargs):
        body = args[3]

        message = "I'm sorry, i'm not understand your command"
        payload = PayloadDTO("20:00", "text", message)

        if body['payload']['message'].lower() == 'lights on':
            message = "I turned on the lights... don't forget to shut down them"
        elif body['payload']['message'].lower() == 'lights off':
            message = 'Lights are off now'
        elif body['payload']['message'].lower() == 'activate alarm':
            message = "Alarm actived!"
        elif body['payload']['message'].lower() == 'deactivate alarm':
            message = "Alarm deactivated"

        payload.message = message

        responseMessage = ResponseMessageDTO(self.__sensorType, self.__chatId, self.__name, self.__image, payload)

        self.__notify_all_listeners(responseMessage)

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)

    def __notify_all_listeners(self, *args, **kwargs):
        logger.info(f'Notify all {self.__observators.__len__()} listeners')
        for observator in self.__observators:
            logger.info(f'Mo notifico')
            observator.on_notify(*args, **kwargs)
