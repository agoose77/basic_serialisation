from serialiser import WriteStream, Modifier, JSONStreamIO, XMLStreamIO
from io import StringIO
from inspect import getmembers
from pprint import pprint


class Vector:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Vector(x={}, y={}, z={})".format(self.x, self.y, self.z)


class VectorModifier(Modifier):

    name = 'vec'
    modifies = Vector

    @classmethod
    def compose(cls, stream):
        x = stream.read('x')
        y = stream.read('y')
        z = stream.read('z')
        return Vector(x, y, z)

    @classmethod
    def decompose(cls, value, stream):
        stream.write('x', value.x)
        stream.write('y', value.y)
        stream.write('z', value.z)


class StructBuilder(type):

    def __init__(cls, name, bases, attrs):
        fields = dict(getmembers(cls, lambda x: isinstance(x, Field)))
        cls._fields = fields

        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        inst = cls.__new__(cls, *args, **kwargs)
        defaults = {n: f.type() for n, f in cls._fields.items()}
        inst.__dict__.update(defaults)
        cls.__init__(inst, *args, **kwargs)
        return inst


class Field:

    def __init__(self, type_):
        self.type = type_


class Struct(metaclass=StructBuilder):

    def print(self):
        pprint("{}({})".format(self.__class__.__name__, ", "
                               .join(("{}={!r}".format(k, getattr(self, k)) for k in self._fields))))


class StructModifierBase(Modifier):

    @classmethod
    def compose(cls, stream):
        struct = cls.modifies()

        for name in struct._fields:
            value = stream.read(name)
            setattr(struct, name, value)

        return struct

    @classmethod
    def decompose(cls, struct, stream):
        for name in struct._fields:
            value = getattr(struct, name)
            stream.write(name, value)

    @classmethod
    def build(cls, modifies_cls):
        cls_dict = dict(modifies=modifies_cls, name=modifies_cls.__name__)
        return type('{}Modifier'.format(modifies_cls.__name__), (cls,), cls_dict)


class SomeStruct(Struct):
    score = Field(float)
    name = Field(str)
    age = Field(int)
    position = Field(Vector)


if __name__ == '__main__':
    # Build list of modifiers for all Struct subclasses
    struct_modifiers = list(map(StructModifierBase.build, Struct.__subclasses__()))
    modifiers = [VectorModifier] + struct_modifiers

    # Something to serialise
    serialisable = SomeStruct()
    serialisable.score = 99.9
    serialisable.age = 12
    serialisable.name = 'Bob'
    serialisable.position.x = 12

    # Write to a write_stream
    write_stream = WriteStream(modifiers=modifiers)
    # We can do this (below) because we created a modifier that decomposes / composes this class
    write_stream.write('some_serialisable', serialisable)

    # Create stream IO with string object
    string_file = StringIO()
    stream_io_cls = JSONStreamIO
    stream_io = stream_io_cls(string_file)

    # Dump to file
    stream_io.dump(write_stream)

    # Print output data
    print(stream_io_cls.__name__, string_file.getvalue())

    # Reload from data file
    string_file.seek(0)
    read_stream = stream_io.load(modifiers=modifiers)

    # Read directly from stream
    serialisable_2 = read_stream.read('some_serialisable')
    serialisable_2.print()