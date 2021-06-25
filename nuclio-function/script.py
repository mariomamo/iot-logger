import ast

import requests


class Event:
    def __init__(self, body):
        self.__body = body

    @property
    def body(self):
        return self.__body


class Context:
    class __Logger:
        def __init__(self):
            pass

        def info(self, msg):
            print(msg)

    class Response:
        def __init__(self, body="", headers=None, content_type="", status_code=200):
            if headers is None:
                headers = dict()

            print(f'body: {body}\nheaders: {headers}\ncontent_type: {content_type}\nstatus_code: {status_code}')

    def __init__(self):
        self.__logger = self.__Logger()

    @property
    def logger(self):
        return self.__logger


# ########################################### COPY IMPORTS ###########################################
# ===========================================> COPY THIS <===========================================
def handler(context, event):
    body = event.body.decode('UTF-8')
    body = ast.literal_eval(body.__str__())

    headers = {'Content-Type': "application/json", 'Accept': "application/json"}
    payload = {
        "sensorType": body['sensorType'],
        "chatId": body['chatId'],
        "name": body['name'],
        "img": body['img'],
        "payload": {
            "hour": body['payload']['hour'],
            "type": body['payload']['type'],
            "message": body['payload']['message']
        }
    }

    response = requests.get("http://192.168.1.52:4444/iot/logger/sendlog", headers=headers,
                            json=payload)

    return context.Response(body=response.json(),
                            headers={},
                            content_type='application/json',
                            status_code=200)


# ===========================================> END COPY <===========================================

if __name__ == '__main__':
    body = b'{\'sensorType\': \'car\',\'chatId\': \'1\', \'name\': \'Car\', \'img\': \'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Circle-icons-car.svg/1200px-Circle-icons-car.svg.png\', \'payload\': {\'hour\': \'20:00\', \'type\': \'text\', \'message\': "I\'m connected!"}}'
    event = Event(body)
    context = Context()

    handler(context, event)
