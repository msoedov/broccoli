import logging
import inspect

import sys
import types
from .utils import annotated_class, sub_modules

log = logging.getLogger(__package__)


def inject(module, *deps):
    """
    :param module: module instance or module name as string
    :param deps: tuple of dependencies
    :return:
    """
    if isinstance(module, str):
        if module in sys.modules:
            module = sys.modules[module]
        else:
            NameError('{} module not found'.format(module))
    package_modules = sub_modules(module)
    package_namespace = sum([list(vars(m).values()) for m in package_modules],
                            [])
    fn_list = []
    for attr in package_namespace:
        if isinstance(attr, types.FunctionType) and attr.__annotations__:
            fn_list.append(attr)
        elif annotated_class(attr):
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
    :param deps: dependencies tuple
    """
    if not deps:
        log.warning('No deps')
        return False, []
    type_to_dependency = {type(d): d for d in deps}
    detected_dependecies = {}
    signature = inspect.signature(fn)
    annotations = fn.__annotations__
    for val, _type in annotations.items():
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
                            'in annotation: {}{}, resolved: {}'.format(
                                param, fn.__name__, annotations,
                                detected_dependecies))
    if not defaults:
        log.warning('%s%s in %s', fn.__name__, fn.__annotations__, deps)
        return False, []
    fn.__defaults__ = tuple(defaults)
    log.warning("Injected %s to %s%s", defaults, fn.__name__, annotations)
    return True, defaults


class Dependency(object):
    """
    Class decorator that allow inject dependencies to the decorated function with type annotation.
    Accepts an optional kwarg `on_start` to specify the dependency resolver function.
    """
    resolved = None
    injected = False

    def __init__(self, on_start=None):
        super(Dependency, self).__init__()
        self.resolved = ()
        self.on_start = on_start

    def __call__(self, fn):
        injected = False

        def wrapper(*a, **kw):
            nonlocal injected
            if not injected:
                self.resolved = self.start()
                injected = True
                bind(fn, *self.resolved)
            return fn(*a, **kw)

        return wrapper

    def start(self):
        if callable(self.on_start):
            return self.on_start()
        return self.resolved

    def __lshift__(self, on_start):
        if callable(on_start):
            self.on_start = on_start
        elif isinstance(on_start, (list, tuple)):
            self.resolved = tuple(on_start)
        else:
            raise TypeError()
        return self
