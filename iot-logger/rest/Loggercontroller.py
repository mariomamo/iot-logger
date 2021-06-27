import ast
import logging

from flask import request
from flask_restplus import Resource

from dto.RisultatoDTO import RisultatoDTO
from service.SocketIOServer import SocketIOServer

api, param = RisultatoDTO.get_api_and_param("clientrest")
socketIOServer = SocketIOServer()


@api.route('/sendlog')
class Message(Resource):
    logging.basicConfig()
    logger = logging.getLogger(f'{__name__}.log')
    logger.setLevel(logging.INFO)

    @api.doc('get response from a message')
    @api.marshal_list_with(param)
    def get(self):
        payload = request.json
        logging.info(f'Ho ricevuto {payload}')
        print(f'Ho ricevuto {payload}')
        ris = RisultatoDTO()
        ris.setSuccess(200)
        ris.setData(payload)
        socketIOServer.send("message", ast.literal_eval(ris.__str__()))
        return ris
