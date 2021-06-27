from abc import abstractmethod, ABC


class HourPicker(ABC):
    @abstractmethod
    def getHour(self): pass
