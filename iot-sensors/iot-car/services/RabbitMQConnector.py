import ast
import logging

import pika
import requests

from interfaces.Observable import Observable
from interfaces.Observator import Observator

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class RabbitMQConnector(Observable, Observator):

    def __init__(self, name: str, image: str, topic_name: str, send_topic_name: str, topic_id: str, topic_url: str):
        self.__topic_url = topic_url
        self.__name = name
        self.__image = image
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__topic_url))
        receive_topic_name = f'{topic_name}/{topic_id}'
        self.__topic_id = topic_id
        self.__receive_channel = self.__getReceiveChannel(receive_topic_name, connection)
        self.__send_channel = self.__get_send_channel(send_topic_name, connection)
        self.__observators = []
        self.notifyConnectedStatus(send_topic_name, topic_id)
        self.__headers = {'Content-Type': 'application/json'}

    def notifyConnectedStatus(self, send_topic_name, topic_id):
        message = self.__getResponseMEssage("text", "I'm connected!", asString=False)
        logger.info(f'Sent on {send_topic_name} value {message}')
        self.__send_channel.basic_publish(exchange="", routing_key=send_topic_name,
                                          body=message)

    def __callBack(self, channel, method, properties, body):
        body = ast.literal_eval(body.decode("UTF-8").__str__())
        logger.info(f'Received from queue {body}')
        output = self.__getResponseMEssage("text", "Command not found")

        if body['payload']['message'].lower() == 'position':
            output = self.__getResponseMEssage("text", "This is my position {position}")
        elif body['payload']['message'].lower() == 'turn off engine':
            output = self.__getResponseMEssage("text", 'Engine turned off')
        elif body['payload']['message'].lower() == 'turn on engine':
            output = self.__getResponseMEssage("text", "Engine turned on")
        elif body['payload']['message'].lower() == 'status':
            output = self.__getResponseMEssage("text", "Fuel level is 57%")

        requests.get("http://192.168.1.52:4444/iot/logger/sendlog", headers=self.__headers, json=output.__str__())

    def __getResponseMEssage(self, type, message, asString: bool=True):
        payload = {
            "sensorType": "car",
            "chatId": self.__topic_id,
            "name": self.__name,
            "img": self.__image,
            "payload": {
                "hour": "20:00",
                "type": type,
                "message": message
            }
        }

        if not asString:
            payload = bytes(payload.__str__(), encoding="UTF-8")
        return payload

    def __getReceiveChannel(self, topic_name, connection):
        try:
            receiveChannel = connection.channel()
            receiveChannel.queue_declare(queue=topic_name)
            receiveChannel.basic_consume(queue=topic_name, on_message_callback=self.__callBack, auto_ack=True)
            logger.info(f'[RabbitMQConnector] Starting consuming on {topic_name}')
        except Exception as ex:
            logger.error(f'Connection with broker failed!')
            return None

        return receiveChannel

    def __get_send_channel(self, send_topic_name, connection):
        sendChannel = connection.channel()
        sendChannel.queue_declare(queue=send_topic_name)
        return sendChannel

    def __notify_all_listeners(self, *args, **kwargs):
        for observator in self.__observators:
            logger.info(f'Mo notifico')
            observator.on_notify(*args, **kwargs)

    def start(self):
        if self.__receive_channel is not None:
            self.__receive_channel.start_consuming()
        else:
            logger.error(f'Broker is not connected!')

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)

    def on_notify(self, *args, **kwargs):
        logger.info(f'Ricevuto')
        # self.__send_channel.basic_publish(exchange='', routing_key=config_dict['topic_name'],
        #                                   body=bytes(payload.__str__(), encoding="UTF-8"))
