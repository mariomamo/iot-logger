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
        default_message = "I'm sorry, i'm not understand your command"
        userId = body['userId']

        message = {
            "lights on": "I turned on the lights... don't forget to shut down them",
            "lights off": "Lights are off now",
            "activate alarm": "Alarm actived!",
            "deactivate alarm": "Alarm deactivated",
        }.get(body['payload']['message'].lower(), default_message)

        payload = PayloadDTO(self.getHour(), "text", message)

        return ResponseMessageDTO(self.sensorType, self.chatId, self.name, self.image, payload, userId=userId)


if __name__ == '__main__':
    homeSensor = HomeSensor('air-conditioner', 'TEST_CHAT_ID', 'NAME', 'IMAGE', 'SENSOR_TOPIC_NAME')
    print(homeSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'lights on'}}))
    print(homeSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'lights off'}}))
    print(homeSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'activate alarm'}}))
    print(homeSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'deactivate alarm'}}))
    print(homeSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'wrong message'}}))
