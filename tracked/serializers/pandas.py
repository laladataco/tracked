from tracked.serializers.serializer import Serializer


_COMPRESSION = 'gzip'


class NDFrame(Serializer):
    def serialize(self, asset, path):
        import pandas as pd
        asset.to_pickle(path, compression=_COMPRESSION)
        return {'compression': _COMPRESSION}

    def deserialize(self, path, meta):
        import pandas as pd
        return pd.read_pickle(path, **meta)

    def detect(self, asset):
        try:
            import pandas as pd
        except ImportError:
            return False
        return isinstance(asset, pd.core.generic.NDFrame)


Serializer.register('pandas/ndframe', NDFrame())
