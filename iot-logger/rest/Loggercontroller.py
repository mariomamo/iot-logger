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
        socketIOServer.send("message", ris.toJSON())
        return ris
