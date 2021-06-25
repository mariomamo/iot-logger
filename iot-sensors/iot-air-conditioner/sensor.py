import werkzeug
import yaml
from werkzeug.utils import cached_property

from sensors.AirConditionerSensor import CarSensor

werkzeug.cached_property = werkzeug.utils.cached_property
from services.RabbitMQConnector import RabbitMQConnector


def getConfigDict():
    yaml_config_path = "application.yml"
    config_file_yml = open(yaml_config_path)
    return yaml.load(config_file_yml, Loader=yaml.FullLoader)


if __name__ == '__main__':
    config_dict = getConfigDict()
    rabbitMQConnector = RabbitMQConnector(config_dict['name'], config_dict['image'], config_dict['receive_topic_name'],
                                          config_dict['send_topic_name'], config_dict["chat_id"],
                                          config_dict['topic_url'])

    car = CarSensor(config_dict['sensor_type'], config_dict['chat_id'], config_dict['name'], config_dict['image'])

    car.subscribe(rabbitMQConnector)
    rabbitMQConnector.subscribe(car)

    while True:
        pass
