# Basic Serialisation
This example demonstrates how to serialise a data structure without polluting the mechanics of _what_ to serialise with _how_ to serialise it.

Adding support for custom types is depends upon the object. You might consider having the stream try calling "serialise" on any object provided to it, and the "deserialise" method when operating in reverse.
In the case of JSON, a custom JSON encoder may be used. For the XML parser, the `_encode_value` and `_decode_value` methods may be overwritten.

In both the above cases, the deserialiser needs to inspect values to determine if they are custom types. This isn't ideal. Whilst it is cleaner to use JSON as-is, and pay the `object_hook` cost at deserialisation, for
XML we can do better - use tags to indicate the object type (See advanced XML)