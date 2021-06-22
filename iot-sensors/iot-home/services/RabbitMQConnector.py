import ast
import logging

import pika
import requests

from dto.RisultatoDTO import RisultatoDTO
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
        self.__send_channel.basic_publish(exchange="", routing_key=send_topic_name,
                                          body=self.__get_body_payload(topic_id))

        self.__headers = {'Content-Type': "application/json", 'Accept': "application/json"}
        requests.get("http://192.168.1.52:4444/iot/logger/sendlog", headers=self.__headers,
                     json=self.__getResponseMEssage("text", "I'm waiting for a command"))

    def __callBack(self, channel, method, properties, body):
        body = ast.literal_eval(body.decode("UTF-8").__str__())
        output = self.__getResponseMEssage("text", "Command not found")

        if body['payload']['message'].lower() == 'lights on':
            output = self.__getResponseMEssage("text", "Done... don't forget to turn them off ")
        elif body['payload']['message'].lower() == 'lights off':
            output = self.__getResponseMEssage("text", 'Ok!')

        headers = {'Content-Type': "application/json", 'Accept': "application/json"}
        requests.get("http://192.168.1.52:4444/iot/logger/sendlog", headers=headers, json=output.__str__())

    def __getResponseMEssage(self, type, message):
        output = {
            "chatId": self.__topic_id,
            "name": self.__name,
            "ora": "20:00",
            "img": self.__image,
            "payload": {
                "type": type,
                "message": message
            }
        }

        return output

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

    def __get_body_payload(self, topic_id):
        payload = {
            "chatId": topic_id,
            "name": "Phone",
            "ora": "20:00",
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Circle-icons-car.svg/1200px-Circle-icons-car.svg.png",
            "payload": {
                "type": "text",
                "message": "My position is {position}"
            }
        }

        return bytes(payload.__str__(), encoding="UTF-8")

    def on_notify(self, *args, **kwargs):
        logger.info(f'Ricevuto')
        # self.__send_channel.basic_publish(exchange='', routing_key=config_dict['topic_name'],
        #                                   body=bytes(payload.__str__(), encoding="UTF-8"))

    pass
