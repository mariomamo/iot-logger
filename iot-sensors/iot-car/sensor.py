import werkzeug
import yaml
from sensors.AirConditionerSensor import AirConditionerSensor
from sensors.CarSensor import CarSensor
from sensors.HomeSensor import HomeSensor
from werkzeug.utils import cached_property

werkzeug.cached_property = werkzeug.utils.cached_property
from services.RabbitMQConnector import RabbitMQConnector


def getConfigDict():
    yaml_config_path = "application.yml"
    config_file_yml = open(yaml_config_path)
    return yaml.load(config_file_yml, Loader=yaml.FullLoader)


def startSensor(sensor_type, chat_id, sensor_name, sensor_image, send_topic_name, receive_topic_name, topic_url):
    global config_dict
    config_dict = getConfigDict()
    rabbitMQConnector = RabbitMQConnector(sensor_name, sensor_image, receive_topic_name,
                                          send_topic_name, chat_id,
                                          topic_url)

    if sensor_type == "car":
        sensor = CarSensor(sensor_type, chat_id, sensor_name, sensor_image,
                           send_topic_name)
    elif sensor_type == "air-conditioner":
        sensor = AirConditionerSensor(sensor_type, chat_id, sensor_name, sensor_image,
                           send_topic_name)
    elif sensor_type == "home":
        sensor = HomeSensor(sensor_type, chat_id, sensor_name, sensor_image,
                           send_topic_name)

    sensor.subscribe(rabbitMQConnector)
    rabbitMQConnector.subscribe(sensor)


if __name__ == '__main__':
    config_dict = getConfigDict()
    for sensor in config_dict['sensors']:
        startSensor(sensor['sensor_type'], sensor['chat_id'], sensor['name'], sensor['image'],
                    sensor['send_topic_name'], sensor['receive_topic_name'], sensor['topic_url'])

