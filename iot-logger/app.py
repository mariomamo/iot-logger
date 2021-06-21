import socket
from threading import Thread
import yaml
from flask import Flask
import werkzeug
from werkzeug.utils import cached_property
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Blueprint
from flask_restplus import Api
from rest.Loggercontroller import api as loggerapi
from service.SocketIOServer import SocketIOServer

yaml_config_path = "application.yml"
print(f"path {yaml_config_path}")
config_file_yml = open(yaml_config_path)
config_dict = yaml.load(config_file_yml, Loader=yaml.FullLoader)

socketIOServer = SocketIOServer(config_dict['name'])


def runApiServer():
    global api
    # yaml_config_path = os.path.join(os.environ['CATALINA_HOME'], "conf", "configurazioni", "fenice", "chatbot", "application.yml")
    # yaml_config_path = os.path.join(os.environ['APP_HOME'], "application.yml")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # server_port = config_dict['port']
    host_ip = s.getsockname()[0]
    s.close()
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
    app.run(host=host_ip, port=config_dict['port'])
    # PRODUCTION
    # waitress.serve(app, listen=f'{host_ip}:{config_dict["port"]}')


def runSocketIOServer():
    socketIOServer.start()


if __name__ == '__main__':
    Thread(target=runApiServer).start()
    Thread(target=runSocketIOServer).start()
