from abc import ABC, abstractmethod
from collections import OrderedDict


class Stream(ABC):

    def __init__(self, data=None):
        if data is None:
            data = OrderedDict()
        self._data = data

    def write(self, name, value):
        self._data[name] = value

    def read(self, name):
        return self._data[name]

    def substream(self, name):
        try:
            data = self._data[name]

        except KeyError:
            self._data[name] = data = OrderedDict()

        return self.__class__(data)


class StreamIOBase:

    @abstractmethod
    def dump(self, stream):
        pass

    @abstractmethod
    def load(self):
        pass
