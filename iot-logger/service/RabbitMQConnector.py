import datetime
import logging

import pika

from interfaces.Observable import Observable
from interfaces.Observator import Observator
from utility.HourPickerImpl import HourPickerImpl

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


class RabbitMQConnector(Observable, Observator):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, topic_name: str, send_topic_name: str, topic_url: str):
        self.__hourPicker = HourPickerImpl()
        self.__receive_topic_name = topic_name
        self.__send_topic_name = send_topic_name
        self.__topic_url = topic_url
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(self.__topic_url))
        # self.__channel = self.__getReceiveChannel()
        self.__observators = []
        self.__sendChannels = {}

    # def __callBack(self, channel, method, properties, body):
    #     ris = RisultatoDTO()
    #     ris.setSuccess(200)
    #     body = ast.literal_eval(body.decode("UTF-8").__str__())
    #     logger.info(f'New message received from topic {self.__receive_topic_name} = {body}')
    #     ris.setData(body)
    #     self.__notify_all_listeners(channel, method, properties, ris)

    # def __getReceiveChannel(self):
    #     try:
    #         channel = self.__connection.channel()
    #         channel.queue_declare(queue=self.__receive_topic_name)
    #         channel.basic_consume(queue=self.__receive_topic_name, on_message_callback=self.__callBack, auto_ack=True)
    #         logger.info(f'[RabbitMQConnector] Starting consuming')
    #     except Exception as ex:
    #         logger.error(f'Connection with broker failed!')
    #         return None
    #
    #     return channel

    def __get_send_channel(self, send_topic_name, connection):
        sendChannel = connection.channel()
        sendChannel.queue_declare(queue=send_topic_name)
        return sendChannel

    # def start(self):
    #     if self.__channel is not None:
    #         self.__channel.start_consuming()
    #     else:
    #         logger.error(f'Broker is not connected!')

    def subscribe(self, observator: Observator):
        self.__observators.append(observator)

    def __get_body_payload(self, body):
        payload = {
            "userId": body['userId'],
            "chatId": body['chatId'],
            "ora": f'{self.__hourPicker.getHour()}',
            "payload": {
                "type": body['payload']['type'],
                "message": body['payload']['message']
            }
        }

        return bytes(payload.__str__(), encoding="UTF-8")

    def on_notify(self, *args, **kwargs):
        body = args[0]
        logger.info(f'Recevied {body}')
        chatId = body['chatId']
        send_topic_name = f'{self.__send_topic_name}/{chatId}'
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__topic_url))
        if chatId not in self.__sendChannels:
            self.__sendChannels[chatId] = self.__get_send_channel(send_topic_name, connection)

        sendChannel = self.__sendChannels[chatId]
        if sendChannel.connection.is_closed:
            self.__sendChannels[chatId] = self.__get_send_channel(send_topic_name, connection)
        sendChannel = self.__sendChannels[chatId]

        body = self.__get_body_payload(body)

        logger.info(f'Sending {body.decode("utf8")}')

        sendChannel.basic_publish(exchange="", routing_key=send_topic_name,
                                  body=body)

    def __notify_all_listeners(self, *args, **kwargs):
        for observator in self.__observators:
            logger.info(f'Mo notifico')
            observator.on_notify(*args, **kwargs)
