import ast
import json

from flask import request
from flask_restplus import Resource
from dto.RisultatoDTO import RisultatoDTO
from service.SocketIOServer import SocketIOServer

api, param = RisultatoDTO.get_api_and_param("clientrest")
socketIOServer = SocketIOServer()


@api.route('/sendlog')
class Message(Resource):
    @api.doc('get response from a message')
    @api.marshal_list_with(param)
    def get(self):
        payload = request.json
        ris = RisultatoDTO()
        ris.setSuccess(200)
        ris.setData(payload)
        print(payload)
        socketIOServer.send("message", ast.literal_eval(ris.__str__()))
        return ris
