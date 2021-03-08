import json
import os.path
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile, TemporaryDirectory
from pathlib import Path
from shutil import copyfile

from tracked.serializers import serialize, deserialize
from tracked.utils import parse_name


class Experiment(object):
    def __init__(self, manifest, store):
        self.manifest = manifest
        self.store = store

    @property
    def name(self):
        return self.manifest['name']

    @property
    def evaluation(self):
        return self.manifest['evaluation']

    def fetch_asset(self, name):
        return self.store.pull_asset(self.name, name, self.manifest['assets'][name])


class Store(ABC):
    def __init__(self, prefix, pulled_asset_dir):
        self.prefix = prefix
        self.pulled_asset_dir = pulled_asset_dir

    def push(self, raw):
        asset_manifest = self._push_assets(raw['name'], raw['assets'])
        manifest = {**raw, 'assets': asset_manifest}
        key = self._generate_key(raw['name'], 'manifest.json')
        with NamedTemporaryFile() as tempfile:
            with open(tempfile.name, 'w') as f:
                json.dump(manifest, f)
                f.write('\n')
            self._push_object(key, tempfile.name)
        return Experiment(manifest, self)

    def pull(self, experiment_name):
        key = self._generate_key(experiment_name, 'manifest.json')
        with NamedTemporaryFile() as tempfile:
            self._pull_object(key, tempfile.name)
            with open(tempfile.name, 'r') as f:
                manifest = json.load(f)
                return Experiment(manifest, self)

    def pull_asset(self, experiment_name, name, asset):
        namespaced_asset_dir = Path(self.pulled_asset_dir) / experiment_name
        namespaced_asset_dir.mkdir(parents=True, exist_ok=True)
        filename = str(namespaced_asset_dir / name)
        key = self._generate_key(experiment_name, 'assets', name)
        self._pull_object(key, filename)
        return deserialize(asset['kind'], filename, asset['meta'])

    def _push_assets(self, experiment_name, assets):
        summary = {}
        with TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)
            for name, asset in assets.items():
                key = self._generate_key(experiment_name, 'assets', name)
                filename = str(tempdir_path / name)
                kind, meta = serialize(asset, filename)
                self._push_object(key, filename)
                summary[name] = {'kind': kind, 'meta': meta}
        return summary

    def _generate_key(self, name, *parts):
        prefix_parts = [] if self.prefix is None else [self.prefix]
        return '/'.join(prefix_parts + parse_name(name) + list(parts))

    @abstractmethod
    def _push_object(self, key, filename):
        pass

    @abstractmethod
    def _pull_object(self, key, filename):
        pass


class LocalStore(Store):
    def __init__(self, dir, prefix=None, pulled_asset_dir=os.path.expanduser('~/.tracked/assets')):
        super().__init__(prefix, pulled_asset_dir)
        self.dir = dir

    def _push_object(self, key, filename):
        full_path = Path(self.dir) / key
        full_path.parent.mkdir(parents=True, exist_ok=True)
        copyfile(filename, full_path)

    def _pull_object(self, key, filename):
        copyfile(Path(self.dir) / key, filename)


class S3Store(Store):
    def __init__(self, bucket, prefix=None, pulled_asset_dir=os.path.expanduser('~/.tracked/assets')):
        super().__init__(prefix, pulled_asset_dir)
        self.bucket = bucket

    def _push_object(self, key, filename):
        self.bucket.upload_file(filename, key)

    def _pull_object(self, key, filename):
        self.bucket.download_file(key, filename)


class GCSStore(Store):
    def __init__(self, bucket, prefix=None, pulled_asset_dir=os.path.expanduser('~/.tracked/assets')):
        super().__init__(prefix, pulled_asset_dir)
        self.bucket = bucket

    def _push_object(self, key, filename):
        self.bucket.blob(key).upload_from_filename(filename)

    def _pull_object(self, key, filename):
        self.bucket.blob(key).download_to_filename(filename)
