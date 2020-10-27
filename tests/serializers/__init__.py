from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path

from annoy import AnnoyIndex
from sklearn.ensemble import RandomForestClassifier
from torch.nn import Linear
from torch import tensor, equal
import numpy as np
import pandas as pd

from tracked.serializers import serialize, deserialize
from tracked.exceptions import SerializerNotFoundError


class _Unknown(object):
    pass


class TestSerializers(TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_annoy_index(self):
        asset = AnnoyIndex(8)
        asset.build(4)
        path = Path(self.tempdir.name) / 'annoy-index'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized.f, asset.f)

    def test_python_str(self):
        asset = 'value'
        path = Path(self.tempdir.name) / 'python-str'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized, asset)

    def test_python_dict(self):
        asset = {'key': 'value'}
        path = Path(self.tempdir.name) / 'python-dict'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized, asset)

    def test_python_list(self):
        asset = [1, 2]
        path = Path(self.tempdir.name) / 'python-list'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized, asset)

    def test_python_set(self):
        asset = {1, 2}
        path = Path(self.tempdir.name) / 'python-set'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized, asset)

    def test_python_tuple(self):
        asset = (1, 2)
        path = Path(self.tempdir.name) / 'python-tuple'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized, asset)

    def test_numpy_array(self):
        asset = np.array([1,2])
        path = Path(self.tempdir.name) / 'numpy-array'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized.all(), asset.all())

    def test_pytorch_module(self):
        asset = Linear(4, 2)
        path = Path(self.tempdir.name) / 'pytorch-module'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized.in_features, asset.in_features)
        self.assertEqual(deserialized.out_features, asset.out_features)

    def test_pytorch_tensor(self):
        asset = tensor([[1., -1.], [1., -1.]])
        path = Path(self.tempdir.name) / 'pytorch-tensor'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertTrue(equal(deserialized, asset))

    def test_sklearn_estimator(self):
        asset = RandomForestClassifier(8)
        path = Path(self.tempdir.name) / 'sklearn-estimator'
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized.n_estimators, asset.n_estimators)

    def test_pandas_data_frame(self):
        asset = pd.DataFrame({'a': [1]})
        path = str(Path(self.tempdir.name) / 'pandas-data-frame')
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized['a'].iloc[0], 1)

    def test_pandas_series(self):
        asset = pd.Series([1])
        path = str(Path(self.tempdir.name) / 'pandas-series')
        kind, meta = serialize(asset, path)
        deserialized = deserialize(kind, path, meta)
        self.assertEqual(deserialized.iloc[0], 1)

    def test_unknown_serialize(self):
        asset = _Unknown()
        path = Path(self.tempdir.name) / 'unknown'
        with self.assertRaises(SerializerNotFoundError):
            serialize(asset, path)

    def test_unknown_deserialize(self):
        path = Path(self.tempdir.name) / 'unknown'
        with self.assertRaises(SerializerNotFoundError):
            deserialize('unknown/unknown', path, None)
