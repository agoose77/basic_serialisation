from stream import ReadStream
from stream_io import StreamFileIOBase

from json import dump, load


class JSONStreamIO(StreamFileIOBase):

    def dump(self, stream):
        as_dict = stream._data
        dump(as_dict, self._file)

    def load(self, **kwargs):
        raw_data = load(self._file)

        return ReadStream(raw_data, **kwargs)
