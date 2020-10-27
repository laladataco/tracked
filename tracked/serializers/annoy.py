from tracked.serializers.serializer import Serializer


class Index(Serializer):
    def detect(self, asset):
        try:
            from annoy import AnnoyIndex
        except ImportError:
            return False
        return isinstance(asset, AnnoyIndex)

    def serialize(self, asset, path):
        asset.save(str(path))
        return {'f': asset.f}

    def deserialize(self, path, meta):
        from annoy import AnnoyIndex
        index = AnnoyIndex(meta['f'])
        index.load(str(path))
        return index


Serializer.register('annoy/index', Index())
