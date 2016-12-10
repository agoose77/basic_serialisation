# Basic Serialisation
This example demonstrates how to serialise a data structure without polluting the mechanics of _what_ to serialise with _how_ to serialise it.

Adding support for custom types depends upon the object. You might consider having the stream try calling "serialise" on any object provided to it, and the "deserialise" method when operating in reverse, but then you need to tag the stream with the object class (just as is done in Pickle).
To avoid this, be explicit. Just call the serialise method yourself.

There are XML and JSON serialisers given as an example. Custom implicit serialisers are defined using "modifiers", which associate with a class type (see `stream.Modifier` abstract base class). An example is given of using a stream Modifier for serialising Vectors (in this case, my own class, but analogous to the Blender `mathutils.Vector` class).