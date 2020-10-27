from tracked.serializers.serializer import Serializer


class Base(Serializer):
    def serialize(self, asset, path):
        import numpy as np
        with open(path, 'wb') as f:
            return np.save(f, asset)

    def deserialize(self, path, meta):
        import numpy as np
        with open(path, 'rb') as f:
            return np.load(f)


class Array(Base):
    def detect(self, asset):
        try:
            import numpy as np
        except ImportError:
            return False
        return type(asset) == np.ndarray


Serializer.register('numpy/array', Array())
