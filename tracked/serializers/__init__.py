import tracked.serializers.annoy
import tracked.serializers.sklearn
import tracked.serializers.python
import tracked.serializers.pytorch
import tracked.serializers.numpy
import tracked.serializers.pandas
from tracked.serializers.serializer import Serializer
from tracked.exceptions import SerializerNotFoundError


def serialize(asset, path):
    for kind, serializer in Serializer.registry.items():
        if serializer.detect(asset):
            return kind, serializer.serialize(asset, path)
    raise SerializerNotFoundError(f'Matching serializer not found for {asset}')


def deserialize(kind, path, meta):
    if kind not in Serializer.registry:
        raise SerializerNotFoundError(f'Matching serializer not found: {kind}')
    return Serializer.registry[kind].deserialize(path, meta)
