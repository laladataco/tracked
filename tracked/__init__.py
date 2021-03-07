from typing import Callable, Tuple

from tracked.utils import generate_name, current_timestamp


def run(store, family, callable: Callable[..., Tuple[dict, dict]], name=None, **kwargs):
    if name is None:
        name = generate_name(family)
    started = current_timestamp()
    assets, evaluation = callable(**kwargs)
    ended = current_timestamp()
    return store.push({
        'name': name,
        'started': started,
        'ended': ended,
        'kwargs': kwargs,
        'assets': assets,
        'evaluation': evaluation
    })
