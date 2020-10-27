import os
import binascii
from time import time


def current_timestamp():
    return int(time())


def generate_name(family):
    timestamp = current_timestamp()
    hex = binascii.b2a_hex(os.urandom(3)).decode('ascii')
    return f'{family}--{timestamp}-{hex}'
