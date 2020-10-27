from unittest import TestCase
from tempfile import TemporaryDirectory

from tracked import run
from tracked.stores import LocalStore


class TestRoot(TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_run_with_args_and_kwargs(self):
        def fake(iterations, num_trees=3):
            return {
                'model': 'test',
                'config': {
                    'iterations': iterations,
                    'num_trees': num_trees
                }
            }, {
                'accuracy': 0.99
            }
        
        store = LocalStore(self.tempdir.name)
        experiment = run(store, 'tracked-testing-fake-1', fake, 100, num_trees=4)
        model = experiment.fetch_asset('model')
        config = experiment.fetch_asset('config')
        self.assertEqual(model, 'test')
        self.assertEqual(config['iterations'], 100)
        self.assertEqual(config['num_trees'], 4)
        self.assertEqual(experiment.evaluation['accuracy'], 0.99)

    def test_run_with_no_args_and_no_kwargs(self):
            def fake():
                return {
                    'model': 'test'
                }, {
                    'accuracy': 0.99
                }
            
            store = LocalStore(self.tempdir.name)
            experiment = run(store, 'tracked-testing-fake-1', fake)
            model = experiment.fetch_asset('model')
            self.assertEqual(model, 'test')
            self.assertEqual(experiment.evaluation['accuracy'], 0.99)

    def test_run_with_args_only(self):
            def fake(num_trees):
                return {
                    'model': 'test',
                    'config': {
                        'num_trees': num_trees
                    }
                }, {
                    'accuracy': 0.99
                }
            
            store = LocalStore(self.tempdir.name)
            experiment = run(store, 'tracked-testing-fake-1', fake, 4)
            model = experiment.fetch_asset('model')
            config = experiment.fetch_asset('config')
            self.assertEqual(model, 'test')
            self.assertEqual(config['num_trees'], 4)
            self.assertEqual(experiment.evaluation['accuracy'], 0.99)

    def test_run_with_kwargs_only(self):
            def fake(num_trees=3):
                return {
                    'model': 'test',
                    'config': {
                        'num_trees': num_trees
                    }
                }, {
                    'accuracy': 0.99
                }
            
            store = LocalStore(self.tempdir.name)
            experiment = run(store, 'tracked-testing-fake-1', fake, num_trees=4)
            model = experiment.fetch_asset('model')
            config = experiment.fetch_asset('config')
            self.assertEqual(model, 'test')
            self.assertEqual(config['num_trees'], 4)
            self.assertEqual(experiment.evaluation['accuracy'], 0.99)        
