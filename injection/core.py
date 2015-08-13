import logging
import inspect

import sys
import types


log = logging.getLogger(__package__)


def inject(module, *deps):
    if isinstance(module, str):
        module = sys.modules[module]
    fn_list = []
    for attr in vars(module).values():
        if isinstance(attr, types.FunctionType):
            fn_list.append(attr)
    for fn in fn_list:
        injected, vals = bind(fn, *deps)
        if injected:
            log.debug("Injected {} -> {}".format(vals, fn.__name__))


def bind(fn, *deps):
    """
    :param: fn - function or method
    """
    if not deps:
        log.warning('No deps')
        return False, []
    type_to_dependency = {type(d): d for d in deps}
    detected_dependecies = {}
    signature = inspect.signature(fn)
    for val, _type in fn.__annotations__.items():
        dep = type_to_dependency.get(_type)
        if dep is None:
            continue
        detected_dependecies[val] = dep
    defaults = []
    for param in signature.parameters:
        if param in detected_dependecies:
            defaults.append(detected_dependecies[param])
    if not defaults:
        log.warning('%s', deps)
        return False, []
    fn.__defaults__ = tuple(defaults)
    log.debug('fn: %s, deps: %s, all: %s', fn, defaults, deps)
    return True, defaults
