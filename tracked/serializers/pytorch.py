from tracked.serializers.serializer import Serializer


class Base(Serializer):
    def serialize(self, asset, path):
        import torch
        asset.to('cpu')
        torch.save(asset, path)

    def deserialize(self, path, meta):
        import torch
        return torch.load(path)


class Module(Base):
     def detect(self, asset):
        try:
            import torch
        except ImportError:
            return False
        return isinstance(asset, torch.nn.Module)

Serializer.register('pytorch/module', Module())


class Tensor(Base):
     def detect(self, asset):
        try:
            import torch
        except ImportError:
            return False
        return isinstance(asset, torch.Tensor)


Serializer.register('pytorch/tensor', Tensor())
