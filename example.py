from stream import Stream
from io import StringIO

from json_io import JSONStreamIO
from xml_io import XMLStreamIO


class SerialisableExample:

    def __init__(self):
        self.score = 0
        self.name = None
        self._hobby = 'skiing'

    def write(self, stream):
        stream.write('score', self.score)
        stream.write('name', self.name)

        stream.substream('secret').write('hobby', self._hobby)

    def read(self, stream):
        self.score = stream.read('score')
        self.name = stream.read('name')

        self._hobby = stream.substream('secret').read('hobby')


def dump_to_string(resource_cls, stream):
    io = StringIO()
    resource = resource_cls(io)
    resource.dump(stream)
    io.seek(0)
    return io.read()


if __name__ == '__main__':
    serialisable = SerialisableExample()

    stream = Stream()
    serialisable.write(stream)

    xml = dump_to_string(XMLStreamIO, stream)
    json = dump_to_string(JSONStreamIO, stream)

    reader = XMLStreamIO(StringIO(xml))
    stream = reader.load()

    serialisable.score = 99
    serialisable.name = 'Jack'
    serialisable._hobby = 'polo'

    serialisable.read(stream)
    print(serialisable.__dict__)
