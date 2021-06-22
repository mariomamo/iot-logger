from abc import ABC, abstractmethod


class Observator(ABC):

    @abstractmethod
    def on_notify(self, *args, **kwargs): pass
