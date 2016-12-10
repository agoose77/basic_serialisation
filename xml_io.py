import xml.etree.ElementTree as ET
from stream import ReadStream
from stream_io import StreamFileIOBase
from ast import literal_eval
from collections import OrderedDict


class XMLStreamIO(StreamFileIOBase):
    _root_text = "savedata"
    _encoding = "us-ascii"

    def _dump_element(self, parent, as_dict):
        for key, value in as_dict.items():
            # Skip this field
            if key == "modifier_name":
                parent.set('modifier', value)
                continue

            child = ET.SubElement(parent, key)

            # Substream
            if isinstance(value, dict):
                self._dump_element(child, value)

            else:
                child.text = repr(value)

    def _load_element(self, parent, as_dict):
        for elem in parent:
            name = elem.tag
            value_text = elem.text

            # Substream
            if value_text is None:
                modifier_name = elem.get('modifier')
                value = {}
                self._load_element(elem, value)
                value['modifier_name'] = modifier_name

            else:
                value = literal_eval(value_text)

            as_dict[name] = value

    def dump(self, stream):
        as_dict = stream._data

        root = ET.Element(self._root_text)
        self._dump_element(root, as_dict)

        as_text = ET.tostring(root, encoding=self._encoding).decode(self._encoding)
        self._file.write(as_text)

    def load(self, **kwargs):
        as_text = self._file.read()
        root = ET.XML(as_text)
        assert root.tag == self._root_text

        data = OrderedDict()
        self._load_element(root, data)

        reader = ReadStream(data, **kwargs)
        return reader

