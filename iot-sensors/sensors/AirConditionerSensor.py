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

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    def message_handler(self, body):
        userId = body['userId']
        default_function = (lambda: "I'm sorry, I'm not understand your command", )

        function = {
            'set 20°': (self.__set_temperature_and_return_message, 20),
            'set 22°': (self.__set_temperature_and_return_message, 22),
            'set 24°': (self.__set_temperature_and_return_message, 24),
            'set 26°': (self.__set_temperature_and_return_message, 26),
            'set 28°': (self.__set_temperature_and_return_message, 28),
            'set 30°': (self.__set_temperature_and_return_message, 30),
            'status': (lambda: f'The temperature is {self.__status}°', )
        }.get(body['payload']['message'].lower(), default_function)

        params = function[1:]
        message = function[0](*params)

        payload = PayloadDTO(self.getHour(), "text", message)
        return ResponseMessageDTO(self.sensorType, self.chatId, self.name, self.image, payload, userId=userId)

    def __set_temperature_and_return_message(self, temp):
        self.__status = temp
        return f'Temperature setted to {self.__status}°'


if __name__ == '__main__':
    airConditionerSensor = AirConditionerSensor('air-conditioner', 'TEST_CHAT_ID', 'NAME', 'IMAGE', 'SENSOR_TOPIC_NAME')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'set 20°'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'set 22°'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'set 24°'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'set 26°'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'set 28°'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'set 30°'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'status'}}))
    print(f'Status: {airConditionerSensor.status}')
    print(airConditionerSensor.message_handler({'userId': 'USER_ID', 'payload': {'message': 'wrong message'}}))
