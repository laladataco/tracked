from tracked.serializers.serializer import Serializer


class Estimator(Serializer):
    def detect(self, asset):
        try:
            import sklearn
            import joblib
        except ImportError:
            return False
        if hasattr(sklearn, 'calibration'):
            return isinstance(asset, (sklearn.base.BaseEstimator, sklearn.calibration._CalibratedClassifier))
        else:
            return isinstance(asset, sklearn.base.BaseEstimator)

    def serialize(self, asset, path):
        import sklearn
        import joblib
        joblib.dump(asset, path)

    def deserialize(self, path, meta):
        import sklearn
        import joblib
        return joblib.load(path)


Serializer.register('sklearn/estimator', Estimator())
