import imp
from unittest import TestCase
from broccoli import inject
from .fixtures.test_module import *
from .fixtures import test_module as m


class TestInject(TestCase):

    def setUp(self):
        imp.reload(m)

    def test_inject_error(self):
        with self.assertRaises(TypeError):
            to_inject = new_app()
            inject(m, *to_inject)

    def test_inject_by_module(self):
        m.do_stuff = lambda: None
        to_inject = new_app()
        inject(m, *to_inject)

        request('foo')
        validation('bar')
        update_query()

    def test_inject_by_module_name(self):
        m.do_stuff = lambda: None
        to_inject = new_app()
        inject('tests.fixtures.test_module', *to_inject)

        request('foo')
        validation('bar')
        update_query()

    def test_inject_by_package_name(self):
        m.do_stuff = lambda: None
        to_inject = new_app()
        inject('tests.fixtures', *to_inject)

        request('foo')
        validation('bar')
        update_query()
