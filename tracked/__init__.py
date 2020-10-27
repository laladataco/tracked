from typing import Callable, Tuple

from tracked.utils import generate_name, current_timestamp


def run(store, family, callable: Callable[[dict], Tuple[dict, dict]], *args, **kwargs):
    name = generate_name(family)
    started = current_timestamp()
    assets, evaluation = callable(*args, **kwargs)
    ended = current_timestamp()
    return store.push({
        'name': name,
        'started': started,
        'ended': ended,
        'args': args,
        'kwargs': kwargs,
        'assets': assets,
        'evaluation': evaluation
    })
