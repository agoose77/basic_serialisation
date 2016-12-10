class StreamFileIOBase:

    def __init__(self, file):
        self._file = file

    def close(self):
        self._file.close()