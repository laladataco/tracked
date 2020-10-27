from abc import ABC, abstractmethod


class Serializer(ABC):
    registry = {}

    @classmethod
    def register(cls, kind, serializer):
        cls.registry[kind] = serializer

    @classmethod
    def unregister(cls, kind):
        cls.registry.pop(kind, None)

    @abstractmethod
    def detect(self, asset):
        pass

    @abstractmethod
    def serialize(self, asset, path):
        pass

    @abstractmethod
    def deserialize(self, path, meta):
        pass
