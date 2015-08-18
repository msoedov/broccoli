import logging
import inspect

import sys
import types

log = logging.getLogger(__package__)


def annotated_class(val):
    return isinstance(val, type) and hasattr(val, '__init__') and hasattr(
        val.__init__, '__annotations__') and val.__init__.__annotations__


def inject(module, *deps):
    """
    :param module:
    :param deps:
    :return:
    """
    if isinstance(module, str):
        module = sys.modules[module]
    fn_list = []
    for attr in vars(module).values():
        if isinstance(attr, types.FunctionType) and attr.__annotations__:
            fn_list.append(attr)
        elif annotated_class(attr):
            # todo: handle method annotations
            fn_list.append(attr.__init__)
    return bind_batch(fn_list, *deps)


def bind_batch(fn_list, *deps):
    for fn in fn_list:
        injected, vals = bind(fn, *deps)
        if injected:
            log.debug("Injected {} -> {}".format(vals, fn.__name__))


def bind(fn, *deps):
    """
    :param fn: annotated function
    :param deps: dependencies
    """
    if not deps:
        log.warning('No deps')
        return False, []
    type_to_dependency = {type(d): d for d in deps}
    detected_dependecies = {}
    signature = inspect.signature(fn)
    annotaions = fn.__annotations__
    for val, _type in annotaions.items():
        dep = type_to_dependency.get(_type)
        if dep is None:
            continue
        detected_dependecies[val] = dep
    defaults = []
    ord_param_names = reversed([p for p in signature.parameters])
    for param in ord_param_names:
        if param in detected_dependecies:
            defaults.append(detected_dependecies[param])
        elif len(detected_dependecies) > len(defaults):
            raise TypeError('Not found mandatory value for `{}`'
                            'in annotaion: {}{}, resolved: {}'.format(
                                param, fn.__name__, annotaions,
                                detected_dependecies))
    if not defaults:
        log.warning('%s%s in %s', fn.__name__, fn.__annotations__, deps)
        return False, []
    fn.__defaults__ = tuple(defaults)
    log.warning("Injected %s to %s%s", defaults, fn.__name__, annotaions)
    return True, defaults


class Dependency(object):
    """docstring for Dependency"""
    resolved = None
    injected = False

    def __init__(self, on_start=None):
        super(Dependency, self).__init__()
        self.resolved = ()
        self.on_start = on_start

    def __call__(self, fn):
        def wrapper(*a, **kw):
            if not self.injected:
                self.resolved = self.start()
                self.injected = True
                bind(fn, *self.resolved)
            return fn(*a, **kw)

        return wrapper

    def start(self):
        if callable(self.on_start):
            return self.on_start()
        return self.resolved

    def __lshift__(self, on_start):
        assert callable(on_start)
        self.on_start = on_start
        return self