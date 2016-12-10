from abc import ABC, abstractmethod, abstractstaticmethod, abstractproperty
from collections import namedtuple


basic_types = (str, int, bool, float, complex, type(None))
forbidden_names = {"modifier_name"}


class Modifier(ABC):

    name = abstractproperty()
    modifies = abstractproperty()

    @abstractstaticmethod
    def decompose(value, stream):
        pass

    @abstractstaticmethod
    def compose(stream):
        pass


class StreamBase(ABC):

    def __init__(self, data=None, modifiers=None):
        if data is None:
            data = {}

        if modifiers is None:
            modifiers = []

        self._type_to_modifier = {m.modifies: m for m in modifiers}
        self._name_to_modifier = {m.name: m for m in modifiers}
        self._modifiers = modifiers

        self._data = data

    def substream(self, name):
        try:
            data = self._data[name]

        except KeyError:
            self._data[name] = data = {}

        return self.__class__(data, modifiers=self._modifiers)


class ReadStream(StreamBase):

    def read(self, name):
        value = self._data[name]

        if isinstance(value, dict):
            if 'modifier_name' in value:
                substream = self.__class__(data=value, modifiers=self._modifiers)

                modifier_name = value['modifier_name']
                modifier = self._name_to_modifier[modifier_name]
                value = modifier.compose(substream)

            else:
                raise ValueError("Cannot read substream")

        return value


class WriteStream(StreamBase):

    def write(self, name, value):
        if name in forbidden_names:
            raise ValueError("Forbidden name {!r}".format(name))

        if not isinstance(value, basic_types):
            type_cls = value.__class__

            try:
                modifier = self._type_to_modifier[type_cls]

            except KeyError:
                raise TypeError("Value must be str, int, bool, complex, float, NoneType or modifiable, not {!r}"
                                .format(type_cls))

            substream = self.__class__(modifiers=self._modifiers)
            modifier.decompose(value, substream)

            value = substream._data
            value['modifier_name'] = modifier.name

        self._data[name] = value
