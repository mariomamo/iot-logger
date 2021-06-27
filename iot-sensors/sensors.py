import logging
import time

import werkzeug
import yaml
from werkzeug.utils import cached_property

from sensors.AirConditionerSensor import AirConditionerSensor
from sensors.CarSensor import CarSensor
from sensors.HomeSensor import HomeSensor
from utility.HourPickerImpl import HourPickerImpl

werkzeug.cached_property = werkzeug.utils.cached_property
from services.RabbitMQConnector import RabbitMQConnector

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


def getConfigDict():
    yaml_config_path = "application.yml"
    config_file_yml = open(yaml_config_path)
    return yaml.load(config_file_yml, Loader=yaml.FullLoader)


def startSensor(sensor_type, chat_id, sensor_name, sensor_image, send_topic_name, receive_topic_name, topic_url):
    global config_dict
    config_dict = getConfigDict()
    rabbitMQConnector = RabbitMQConnector(sensor_name, sensor_image, receive_topic_name,
                                          send_topic_name, chat_id,
                                          topic_url, HourPickerImpl())

    sensor = None

    if sensor_type == "car":
        sensor = CarSensor(sensor_type, chat_id, sensor_name, sensor_image,
                           send_topic_name)
    elif sensor_type == "air-conditioner":
        sensor = AirConditionerSensor(sensor_type, chat_id, sensor_name, sensor_image,
                                      send_topic_name)
    elif sensor_type == "home":
        sensor = HomeSensor(sensor_type, chat_id, sensor_name, sensor_image,
                            send_topic_name)

    if sensor is not None:
        sensor.subscribe(rabbitMQConnector)
        rabbitMQConnector.subscribe(sensor)
        rabbitMQConnector.start()
    else:
        logger.error(f"Invalid sensor type for {sensor_type}")


if __name__ == '__main__':
    time.sleep(5)
    config_dict = getConfigDict()
    for sensor in config_dict['sensors']:
        startSensor(sensor['sensor_type'], sensor['chat_id'], sensor['name'], sensor['image'],
                    sensor['send_topic_name'], sensor['receive_topic_name'], sensor['topic_url'])

    # while True:
    #     pass
