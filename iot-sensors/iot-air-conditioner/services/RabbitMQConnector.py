import ast
import logging
from threading import Thread

import pika

from interfaces.Observable import Observable
from interfaces.Observator import Observator

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class RabbitMQConnector(Observable, Observator):

    def __init__(self, name: str, image: str, receive_topic_name: str, send_topic_name: str, topic_id: str,
                 topic_url: str):
        self.__topic_url = topic_url
        self.__name = name
        self.__image = image
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__topic_url))
        self.__receive_topic_name = f'{receive_topic_name}/{topic_id}'
        self.__topic_id = topic_id
        self.__send_topic_name = send_topic_name
        self.__send_channel = self.__get_send_channel(send_topic_name, connection)
        self.__receive_channel = self.__getReceiveChannel(self.__receive_topic_name, connection)
        self.__observators = []
        self.notifyConnectedStatus(send_topic_name, topic_id)
        self.__headers = {'Content-Type': 'application/json'}
        self.__start_listening()

    def notifyConnectedStatus(self, send_topic_name, topic_id):
        message = self.__getResponseMEssage("text", "Bed room air conditioner is now online!", asString=False)
        logger.info(f'Sent on {send_topic_name} value {message}')
        self.__send_channel.basic_publish(exchange="", routing_key=send_topic_name,
                                          body=message)

    def __callBack(self, channel, method, properties, body):
        body = ast.literal_eval(body.decode("UTF-8").__str__())
        logger.info(f'New message received from topic {self.__receive_topic_name} = {body}')
        self.__notify_all_listeners(channel, method, properties, body)

    def __getResponseMEssage(self, type, message, asString: bool = True):
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
        logger.info(f'Notify all {self.__observators.__len__()} listeners')
        for observator in self.__observators:
            logger.info(f'Mo notifico')
            observator.on_notify(*args, **kwargs)

    def __start_listening(self):
        if self.__receive_channel is not None:
            Thread(target=lambda: self.__receive_channel.start_consuming()).start()
        else:
            logger.error(f'Broker is not connected!')

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)

    def on_notify(self, *args, **kwargs):
        logger.info(f'Ricevuto {args[0]}')
        self.__send_channel.basic_publish(exchange="", routing_key=self.__send_topic_name,
                                          body=args[0].__str__().encode())
