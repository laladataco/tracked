import os
import binascii
from time import time


def current_timestamp():
    return int(time())


def generate_name(family):
    timestamp = current_timestamp()
    hex = binascii.b2a_hex(os.urandom(3)).decode('ascii')
    return f'{family}__{timestamp}_{hex}'


def parse_name(name):
    if '--' in name:
        return name.rsplit('--', 1)
    else:
        return name.rsplit('__', 1)
