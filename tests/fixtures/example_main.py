from collections import namedtuple

from broccoli import inject

DependencyA = namedtuple('A', '')
DependencyB = namedtuple('B', '')


def foo(a, b: DependencyA):
    return a


def bar(a, b: DependencyB):
    return a


inject(__name__, DependencyA(), DependencyB())

assert foo(1) == 1
assert bar(10) == 10
