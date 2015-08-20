import unittest
from .fixtures.types import *
from broccoli import Dependency


def dependecies():
    return Db(), Service(), Cache()


class CustomDeps(Dependency):

    def start(self):
        return dependecies()


dependency = Dependency(dependecies)

dependency_rshift = Dependency() << dependecies
dependency_rshift_v2 = Dependency() << dependecies()

custom_deps = CustomDeps()


@dependency
def a(db: Db):
    return db


@dependency_rshift
def a_v1(db: Db):
    return db


@custom_deps
def a_v2(db: Db):
    return db


@dependency_rshift_v2
def a_v3(db: Db):
    return db


dbs = [a, a_v1, a_v2, a_v3]


class TestDecorator(unittest.TestCase):

    def test_injected_db(self):
        for fn in dbs:
            val = fn()
            self.assertEqual(val, Db())
