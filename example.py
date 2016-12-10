from stream import WriteStream, ReadStream, Modifier
from io import StringIO

from json_io import JSONStreamIO
from xml_io import XMLStreamIO

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

    @staticmethod
    def compose(stream):
        x = stream.read('x')
        y = stream.read('y')
        z = stream.read('z')
        return Vector(x, y, z)

    @staticmethod
    def decompose(value, stream):
        stream.write('x', value.x)
        stream.write('y', value.y)
        stream.write('z', value.z)


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
    modifiers = [VectorModifier]

    # Something to serialise
    serialisable = SerialisableExample()
    serialisable.hobby = 'water polo'
    serialisable.position.x = 12
    serialisable.name = 'Bob'
    serialisable.score = 99

    # Write to a write_stream
    write_stream = WriteStream(modifiers=modifiers)
    serialisable.write(write_stream)

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

    # Print before load
    print("\nSaved serialisable:")
    serialisable.print()
    del serialisable

    # Now print a clean serialisable
    serialisable = SerialisableExample()
    print("\nNew serialisable:")
    serialisable.print()

    # Print results of load
    serialisable.read(read_stream)
    print("\nLoaded serialisable:")
    serialisable.print()