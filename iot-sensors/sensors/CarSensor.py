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
        self.__position = "40.77443841607973, 14.788751509847078"

    def message_handler(self, body):
        default_message = "I'm sorry, i'm not understand your command"
        userId = body['userId']

        message = {
            "position": f"I'm here {{{self.__position}}}",
            "engine on": "Engine turned on",
            "engine off": "Engine turned off",
            "status": "Fuel level is 57%"
        }.get(body['payload']['message'].lower(), default_message)

        payload = PayloadDTO(self.getHour(), "text", message)

        return ResponseMessageDTO(self.sensorType, self.chatId, self.name, self.image, payload, userId=userId)


if __name__ == '__main__':
    carSensor = CarSensor('air-conditioner', 'TEST_CHAT_ID', 'NAME', 'IMAGE', 'SENSOR_TOPIC_NAME')
    print(carSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'engine on'}}))
    print(carSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'engine OFF'}}))
    print(carSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'PoSitioN'}}))
    print(carSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'status'}}))
    print(carSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'wrong'}}))
