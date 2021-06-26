import logging

from dto.PayloadDTO import PayloadDTO
from dto.ResponseMessageDTO import ResponseMessageDTO
from sensors.Sensor import Sensor

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class AirConditionerSensor(Sensor):
    def __init__(self, sensorType, chatId, name, image, send_topic_name):
        super(AirConditionerSensor, self).__init__(sensorType, chatId, name, image, send_topic_name)
        self.__status = 20

    def message_handler(self, body):
        message = "I'm sorry, i'm not understand your command"
        payload = PayloadDTO(self.getHour(), "text", message)

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

        return ResponseMessageDTO(self.sensorType, self.chatId, self.name, self.image, payload)
