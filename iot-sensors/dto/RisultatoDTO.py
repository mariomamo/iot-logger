import json

from flask_restplus import Namespace, fields


class RisultatoDTO:
    @staticmethod
    def get_api_and_param(name):
        api = Namespace(name, description=f'{name} rest operations')

        param = api.model(name, {
            'success': fields.Boolean(required=True, description='Esito operazione'),
            'code': fields.Integer(required=True, description='Codice risposta http'),
            'descrizione': fields.String(required=True, description='Descrizione operazione'),
            'data': fields.Raw(required=True, description='Dati ottenuti'),
        })
        return api, param

    def __init__(self):
        self.__success: bool = bool()
        self.__code: int = int()
        self.__descrizione: str = str()
        self.__data: object = object()

        self.clear()

    def clear(self):
        self.__success = False
        self.code = 0
        self.__data = None
        self.descrizione = None

    def setSuccess(self, code: int) -> object:
        self.__success = True
        self.__code = code
        return self

    def setError(self, errore: str, code: int) -> object:
        self.__success = False
        self.__descrizione = errore
        self.__code = code
        self.__data = None
        return self

    @property
    def success(self):
        return self.__success

    @property
    def code(self) -> int:
        return self.__code

    @code.setter
    def code(self, code: int) -> None:
        self.__code = code

    @property
    def data(self) -> object:
        return self.__data

    def setData(self, data: object) -> object:
        self.__data = data
        return self.__data

    @property
    def descrizione(self) -> str:
        return self.__descrizione

    @descrizione.setter
    def descrizione(self, descrizione: str) -> None:
        self.__descrizione = descrizione

    def toJSON(self):
        keys = {key[len(__name__) -1:]:value for (key, value) in self.__dict__.items()}
        return json.dumps(self, default=lambda o: keys, sort_keys=True, indent=4)

    def __str__(self):
        string = f"{{\"success:\":\"{self.__success}\", \"code\":\"{self.__code}\""

        if self.__descrizione is not None:
            string += f", \"descrizione\":\"{self.__descrizione}\""
        if self.__data is not None:
            if type(self.__data) is str():
                string += f", \"data\":\"{self.__data}\""
            else:
                string += f", \"data\":{self.__data}"

        string += "}"

        return string


if __name__ == "__main__":
    r = RisultatoDTO()
    # print(r.success(200))
    print(r.error("Erroraccio", 200))
    r.setData("Ciao")
    print(r)
