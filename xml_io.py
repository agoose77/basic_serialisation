import xml.etree.ElementTree as ET
from stream import StreamIOBase, Stream
from ast import literal_eval
from collections import OrderedDict


class XMLStreamIO(StreamIOBase):
    _root_text = "savedata"
    _encoding = "us-ascii"

    def __init__(self, file):
        self._file = file

    def _encode_value(self, value):
        return repr(value)

    def _decode_value(self, value):
        return literal_eval(value)

    def _dump_element(self, parent, as_dict):
        for key, value in as_dict.items():
            child = ET.SubElement(parent, key)
            if isinstance(value, dict):
                self._dump_element(child, value)
            else:
                child.text = self._encode_value(value)

    def _load_element(self, parent, as_dict):
        for elem in parent:
            name = elem.tag
            value = elem.text

            if value is None:
                data = as_dict[name] = OrderedDict()
                self._load_element(elem, data)
            else:
                as_dict[name] = self._decode_value(value)

    def dump(self, stream):
        as_dict = stream._data

        root = ET.Element(self._root_text)
        self._dump_element(root, as_dict)

        as_text = ET.tostring(root, encoding=self._encoding).decode(self._encoding)
        self._file.write(as_text)

    def load(self):
        as_text = self._file.read()
        root = ET.XML(as_text)
        assert root.tag == self._root_text

        data = OrderedDict()
        self._load_element(root, data)
        return Stream(data)