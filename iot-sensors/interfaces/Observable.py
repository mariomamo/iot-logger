from abc import ABC, abstractmethod

from interfaces import Observator


class Observable(ABC):

    @abstractmethod
    def subscribe(self, observator: Observator): pass
