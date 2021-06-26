import logging

from dto.PayloadDTO import PayloadDTO
from dto.ResponseMessageDTO import ResponseMessageDTO
from sensors.Sensor import Sensor

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class CarSensor(Sensor):
    def __init__(self, sensorType, chatId, name, image, send_topic_name):
        super(CarSensor, self).__init__(sensorType, chatId, name, image, send_topic_name)

    def message_handler(self, body):
        message = "I'm sorry, i'm not understand your command"
        payload = PayloadDTO(self.getHour(), "text", message)

        if body['payload']['message'].lower() == 'position':
            message = "This is my position {position}"
        elif body['payload']['message'].lower() == 'engine off':
            message = 'Engine turned off'
        elif body['payload']['message'].lower() == 'engine on':
            message = "Engine turned on"
        elif body['payload']['message'].lower() == 'status':
            message = "Fuel level is 57%"

        payload.message = message

        return ResponseMessageDTO(self.sensorType, self.chatId, self.name, self.image, payload)
