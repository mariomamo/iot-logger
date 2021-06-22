import uuid
from threading import Thread

import werkzeug
import yaml
from werkzeug.utils import cached_property

werkzeug.cached_property = werkzeug.utils.cached_property
from services.RabbitMQConnector import RabbitMQConnector


def getConfigDict():
    yaml_config_path = "application.yml"
    config_file_yml = open(yaml_config_path)
    return yaml.load(config_file_yml, Loader=yaml.FullLoader)


#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=config_dict['topic_url']))
# sendChannel = connection.channel()
# sendChannel.queue_declare(queue=config_dict['topic_name'])
#
# payload = {
#     "chatId": receiving_topic_id,
#     "name": "Phone",
#     "ora": "20:00",
#     "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Circle-icons-car.svg/1200px-Circle-icons-car.svg.png",
#     "payload": {
#         "type": "text",
#         "message": "My position is {position}"
#     }
# }
#
# sendChannel.basic_publish(exchange='', routing_key=config_dict['topic_name'],
#                           body=bytes(payload.__str__(), encoding="UTF-8"))
# print(" [x] Sent 'Hello World!'")
# connection.close()


def runMQTTClient():
    rabbitMQConnector.start()


if __name__ == '__main__':
    config_dict = getConfigDict()
    rabbitMQConnector = RabbitMQConnector(config_dict['name'], config_dict['image'], config_dict['receive_topic_name'],
                                          config_dict['send_topic_name'], config_dict["id"],
                                          config_dict['topic_url'])
    Thread(target=runMQTTClient).start()
