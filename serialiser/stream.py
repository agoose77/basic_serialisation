from abc import ABC, abstractclassmethod, abstractproperty


basic_types = (str, int, bool, float, complex, type(None))
forbidden_names = {"modifier_name"}


class Modifier(ABC):

    name = abstractproperty()
    modifies = abstractproperty()

    @abstractclassmethod
    def compose(cls, stream, context):
        pass

    @abstractclassmethod
    def decompose(cls, value, stream, context):
        pass


class ModifierManager:

    def __init__(self, context=None, modifiers=None):
        if modifiers is None:
            modifiers = []
        if context is None:
            context = {}

        self._modifiers = []
        self._type_to_modifier = {}
        self._name_to_modifier = {}

        self.context = context

        for m in modifiers:
            self.add_modifier(m)

    def add_modifier(self, modifier_cls):
        self._modifiers.append(modifier_cls)
        self._type_to_modifier[modifier_cls.modifies] = modifier_cls
        self._name_to_modifier[modifier_cls.name] = modifier_cls

    def from_name(self, name):
        return self._name_to_modifier[name]

    def from_class(self, cls):
        return self._type_to_modifier[cls]


class StreamBase(ABC):

    def __init__(self, data=None, modifier_manager=None):
        if data is None:
            data = {}

        self._data = data
        self._modifier_manager = modifier_manager

    def substream(self, name):
        try:
            data = self._data[name]

        except KeyError:
            self._data[name] = data = {}

        return self.__class__(data, modifier_manager=self._modifier_manager)


class ReadStream(StreamBase):

    def read(self, name):
        value = self._data[name]

        if isinstance(value, dict):
            if 'modifier_name' in value:
                substream = self.__class__(data=value, modifier_manager=self._modifier_manager)

                modifier_name = value['modifier_name']
                modifier = self._modifier_manager.from_name(modifier_name)
                value = modifier.compose(substream, self._modifier_manager.context)

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
                modifier = self._modifier_manager.from_class(type_cls)

            except KeyError:
                raise TypeError("Value must be str, int, bool, complex, float, NoneType or modifiable, not {!r}"
                                .format(type_cls))

            substream = self.__class__(modifier_manager=self._modifier_manager)
            modifier.decompose(value, substream, self._modifier_manager.context)

            value = substream._data
            value['modifier_name'] = modifier.name

        self._data[name] = value
