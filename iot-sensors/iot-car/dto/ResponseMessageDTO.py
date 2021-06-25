import json
import math


class ResponseMessageDTO:
    def __init__(self, sensorType, chatId, name, image, payload):
        self.__sensorType = sensorType
        self.__chatId = chatId
        self.__name = name
        self.__image = image
        self.__payload = payload

    @property
    def sensorType(self):
        return self.__sensorType

    @property
    def chatId(self):
        return self.__chatId

    @property
    def name(self):
        return self.__name

    @property
    def image(self):
        return self.__image

    @property
    def payload(self):
        return self.__payload

    def __str__(self):
        res = {
            "sensorType": self.__sensorType,
            "chatId": self.__chatId,
            "name": self.__name,
            "img": self.__image,
            "payload": self.__payload.toDict()
        }

        return str(res)
