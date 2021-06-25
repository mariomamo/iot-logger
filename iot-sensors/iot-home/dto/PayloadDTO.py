

class PayloadDTO:
    def __init__(self, hour, type, message):
        self.__hour = hour
        self.__type = type
        self.__message = message

    @property
    def hour(self):
        return self.__hour

    @hour.setter
    def hour(self, hour):
        self.__hour = hour

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        return {
            "hour": self.__hour,
            "type": self.__type,
            "message": self.__message
        }
