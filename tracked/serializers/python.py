import pickle

from tracked.serializers.serializer import Serializer


class Base(Serializer):
    def serialize(self, asset, path):
        with open(path, 'wb') as f:
            pickle.dump(asset, f)

    def deserialize(self, path, meta):
        with open(path, 'rb') as f:
            return pickle.load(f)


class List(Base):
    def detect(self, asset):
        return type(asset) == list


Serializer.register('python/list', List())


class Tuple(Base):
    def detect(self, asset):
        return type(asset) == tuple


Serializer.register('python/tuple', Tuple())


class Set(Base):
    def detect(self, asset):
        return type(asset) == set


Serializer.register('python/set', Set())


class Dict(Base):
    def detect(self, asset):
        return type(asset) == dict


Serializer.register('python/dict', Dict())


class Str(Base):
    def detect(self, asset):
        return type(asset) == str


Serializer.register('python/str', Str())
