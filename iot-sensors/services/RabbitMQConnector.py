import ast
import logging
from threading import Thread

import pika

from dto.PayloadDTO import PayloadDTO
from dto.ResponseMessageDTO import ResponseMessageDTO
from interfaces.Observable import Observable
from interfaces.Observator import Observator
from utility import HourPicker

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class RabbitMQConnector(Observable, Observator, Thread):

    def __init__(self, name: str, image: str, receive_topic_name: str, send_topic_name: str, topic_id: str,
                 topic_url: str, hourPicker: HourPicker):
        Thread.__init__(self)
        self.__name = name
        self.__image = image
        self.__receive_topic_name = f'{receive_topic_name}/{topic_id}'
        self.__send_topic_name = send_topic_name
        self.__topic_id = topic_id
        self.__topic_url = topic_url
        self.__hourPicker = hourPicker
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(self.__topic_url))
        self.__send_channel = self.__get_send_channel(send_topic_name)
        self.__receive_channel = self.__getReceiveChannel(self.__receive_topic_name)
        self.__observators = []
        self.__headers = {'Content-Type': 'application/json'}

    def notifyConnectedStatus(self, sensor_type, send_topic_name, topic_id, image, message):
        payload = PayloadDTO(self.__hourPicker.getHour(), "text", message)
        responseMessageDTO = ResponseMessageDTO(sensor_type, topic_id, self.__name, image, payload)
        logger.info(f'Sent on {send_topic_name} value {responseMessageDTO}')
        self.__send_channel.basic_publish(exchange="", routing_key=send_topic_name,
                                          body=bytes(responseMessageDTO.__str__(), encoding="UTF-8"))

    def __callBack(self, channel, method, properties, body):
        body = ast.literal_eval(body.decode("UTF-8").__str__())
        logger.info(f'New message received from topic {self.__receive_topic_name} = {body}')
        self.__notify_all_listeners("message", channel, method, properties, body)

    def __getReceiveChannel(self, topic_name):
        try:
            receiveChannel = self.__connection.channel()
            receiveChannel.queue_declare(queue=topic_name)
            receiveChannel.basic_consume(queue=topic_name, on_message_callback=self.__callBack, auto_ack=True)
            logger.info(f'[RabbitMQConnector] Starting consuming on {topic_name}')
        except Exception as ex:
            logger.error(f'Connection with broker failed! {ex}')
            return None

        return receiveChannel

    def __get_send_channel(self, send_topic_name):
        sendChannel = self.__connection.channel()
        sendChannel.queue_declare(queue=send_topic_name)
        return sendChannel

    def __notify_all_listeners(self, message, *args, **kwargs):
        logger.info(f'Notify all {self.__observators.__len__()} listeners')
        for observator in self.__observators:
            observator.on_notify(message, *args, **kwargs)

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)
        self.__notify_all_listeners("subscribed")

    def on_notify(self, *args, **kwargs):
        message = args[0]
        if message == "subscribed":
            sensor_type = args[1]
            topicName = args[2]
            chatId = args[3]
            image = args[4]
            message = args[5]
            self.notifyConnectedStatus(sensor_type, topicName, chatId, image, message)
        elif message == "message":
            logger.info(f'Ricevuto {args[1]}')
            self.__send_channel.basic_publish(exchange="", routing_key=self.__send_topic_name,
                                              body=args[1].__str__().encode())

    def run(self) -> None:
        logger.info(f'Starting...')
        if self.__receive_channel is not None:
            self.__receive_channel.start_consuming()
        logger.info(f'Started!')
