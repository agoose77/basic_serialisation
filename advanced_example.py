from serialiser import WriteStream, Modifier, JSONStreamIO, XMLStreamIO
from io import StringIO

from pprint import pprint


class Vector:

    def __init__(self, x, y, z):
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


class StructModifierBase(Modifier):

    @classmethod
    def compose(cls, stream):
        struct = cls.modifies()
        struct.read(stream)
        return struct

    @classmethod
    def decompose(cls, value, stream):
        value.write(stream)

    @classmethod
    def build(cls, modifies_cls):
        cls_dict = dict(modifies=modifies_cls, name=modifies_cls.__name__)
        return type('{}Modifier'.format(modifies_cls.__name__), (cls,), cls_dict)


class SerialisableExample:

    def __init__(self):
        self.score = 0
        self.name = None
        self.position = Vector(1, 2, 3)
        self.hobby = 'skiing'

    def write(self, stream):
        stream.write('score', self.score)
        stream.write('name', self.name)
        stream.write('position', self.position)
        stream.write('hobby', self.hobby)

    def read(self, stream):
        self.score = stream.read('score')
        self.name = stream.read('name')
        self.position = stream.read('position')
        self.hobby = stream.read('hobby')

    def print(self):
        pprint(dict(score=self.score, name=self.name, position=self.position, hobby=self.hobby))


if __name__ == '__main__':
    # Install modifier for the SerialisableExample class
    modifiers = [VectorModifier, StructModifierBase.build(SerialisableExample)]

    # Something to serialise
    serialisable = SerialisableExample()
    serialisable.hobby = 'water polo'
    serialisable.position.x = 12
    serialisable.name = 'Bob'
    serialisable.score = 99

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