import logging
import socket
import time
from threading import Thread

import waitress
import werkzeug
import yaml
from flask import Flask
from werkzeug.utils import cached_property

werkzeug.cached_property = werkzeug.utils.cached_property
from service.RabbitMQConnector import RabbitMQConnector
from flask import Blueprint
from flask_restplus import Api
from rest.Loggercontroller import api as loggerapi
from service.SocketIOServer import SocketIOServer

logging.basicConfig()
logger = logging.getLogger(f'{__name__}.log')
logger.setLevel(logging.INFO)


def getConfigDict():
    yaml_config_path = "application.yml"
    config_file_yml = open(yaml_config_path)
    return yaml.load(config_file_yml, Loader=yaml.FullLoader)


config_dict = getConfigDict()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
# server_port = config_dict['port']
host_ip = s.getsockname()[0]
s.close()


def runApiServer():
    global api
    # yaml_config_path = os.path.join(os.environ['CATALINA_HOME'], "conf", "configurazionhouri", "fenice", "chatbot", "application.yml")
    # yaml_config_path = os.path.join(os.environ['APP_HOME'], "application.yml")
    blueprint = Blueprint('api', __name__)
    api = Api(blueprint,
              title=config_dict['name'],
              version='1.0',
              description='NLP Chatbot application'
              )
    # Creazione endpoints
    api.add_namespace(loggerapi, path='/iot/logger')
    app = Flask(config_dict['name'])
    app.register_blueprint(blueprint)
    app.app_context().push()
    # DEV
    # app.run(host=host_ip, port=config_dict['rest_port'])
    # PRODUCTION
    port = config_dict["rest_port"]
    logger.info(f'[API SERVER RUNNIG] Server running on host {host_ip} and port {port}')
    waitress.serve(app, listen=f'{host_ip}:{port}')


def runSocketIOServer():
    socketIOServer.start(host_ip, config_dict['socket_io_port'])


if __name__ == '__main__':
    time.sleep(10)
    socketIOServer = SocketIOServer(config_dict['name'])
    rabbitMQConnector = RabbitMQConnector(config_dict['receive_topic_name'], config_dict['send_topic_name'],
                                          config_dict['topic_url'])

    socketIOServer.subscribe(rabbitMQConnector)
    rabbitMQConnector.subscribe(socketIOServer)

    Thread(target=runApiServer).start()
    Thread(target=runSocketIOServer).start()

    # while True:
    #     pass
