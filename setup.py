from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(
    name='tracked',
    version=VERSION,
    url='https://github.com/laladataco/tracked',
    description='Track experiments and package assets',
    packages=find_packages(),
    zip_safe=True,
    test_suite='tests',
    tests_require=[
        'joblib==0.13.2',
        'annoy==1.17.0',
        'scikit-learn==0.23.2',
        'torch==1.7.0'
    ]
)
