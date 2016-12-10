from serialiser import WriteStream, JSONStreamIO, XMLStreamIO
from io import StringIO

from pprint import pprint


class SerialisableExample:

    def __init__(self):
        self.score = 0
        self.name = None
        self.hobby = 'skiing'

    def write(self, stream):
        stream.write('score', self.score)
        stream.write('name', self.name)
        stream.write('hobby', self.hobby)

    def read(self, stream):
        self.score = stream.read('score')
        self.name = stream.read('name')
        self.hobby = stream.read('hobby')

    def print(self):
        pprint(dict(score=self.score, name=self.name, hobby=self.hobby))


if __name__ == '__main__':
    # Something to serialise
    serialisable = SerialisableExample()
    serialisable.hobby = 'water polo'
    serialisable.name = 'Bob'
    serialisable.score = 99

    # Write to a write_stream
    write_stream = WriteStream()
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
    read_stream = stream_io.load()

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