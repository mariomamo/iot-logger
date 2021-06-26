import logging
from abc import abstractmethod

from interfaces.Observable import Observable
from interfaces.Observator import Observator
from utility.HourPickerImpl import HourPickerImpl

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class Sensor(Observator, Observable):
    def __init__(self, sensorType, chatId, name, image, send_topic_name):
        self.__sensorType = sensorType
        self.__send_topic_name = send_topic_name
        self.__chatId = chatId
        self.__name = name
        self.__image = image
        self.__observators = []
        self.__hourPickerImpl = HourPickerImpl()

    @property
    def sensorType(self):
        return self.__sensorType

    @sensorType.setter
    def sensorType(self, sensorType):
        self.__sensorType = sensorType

    @property
    def sendTopicName(self):
        return self.__sendTopicName

    @sendTopicName.setter
    def sendTopicName(self, sendTopicName):
        self.__sendTopicName = sendTopicName

    @property
    def chatId(self):
        return self.__chatId

    @chatId.setter
    def chatId(self, chatId):
        self.__chatId = chatId

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    @property
    def observators(self):
        return self.__observators

    @observators.setter
    def observators(self, observators):
        self.__observators = observators

    def getHour(self):
        return self.__hourPickerImpl.getHour()

    @abstractmethod
    def message_handler(self, body: dict):
        pass

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)
        self.__notify_all_listeners("subscribed", self.__sensorType, self.__send_topic_name, self.__chatId,
                                    self.__image, "I'm connected")

    def __notify_all_listeners(self, message, *args, **kwargs):
        logger.info(f'Notify all {self.__observators.__len__()} listeners')
        for observator in self.__observators:
            observator.on_notify(message, *args, **kwargs)

    def on_notify(self, *args, **kwargs):
        message = args[0]
        if message == "subscribed":
            logger.info("A new subsriber is connected")
        elif message == "message":
            body = args[4]

            responseMessage = self.message_handler(body)

            logger.info(f"Invio {responseMessage}")

            self.__notify_all_listeners("message", responseMessage)
