import logging

from dto.PayloadDTO import PayloadDTO
from dto.ResponseMessageDTO import ResponseMessageDTO
from sensors.Sensor import Sensor

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class HomeSensor(Sensor):
    def __init__(self, sensorType, chatId, name, image, send_topic_name):
        super(HomeSensor, self).__init__(sensorType, chatId, name, image, send_topic_name)

    def message_handler(self, body):
        message = "I'm sorry, i'm not understand your command"
        payload = PayloadDTO(self.getHour(), "text", message)
        userId = body['userId']

        if body['payload']['message'].lower() == 'lights on':
            message = "I turned on the lights... don't forget to shut down them"
        elif body['payload']['message'].lower() == 'lights off':
            message = 'Lights are off now'
        elif body['payload']['message'].lower() == 'activate alarm':
            message = "Alarm actived!"
        elif body['payload']['message'].lower() == 'deactivate alarm':
            message = "Alarm deactivated"

        payload.message = message

        return ResponseMessageDTO(self.sensorType, self.chatId, self.name, self.image, payload, userId=userId)
