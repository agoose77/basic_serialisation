from stream import StreamIOBase, Stream
from json import dump, load


class JSONStreamIO(StreamIOBase):

    def __init__(self, file, encoder=None, decoder=None):
        self._file = file
        self._encoder = encoder
        self._decoder = decoder

    def dump(self, stream):
        as_dict = stream._data
        dump(as_dict, self._file, cls=self._encoder)

    def load(self):
        data = load(self._file, object_hook=self._decoder)
        return Stream(data)
