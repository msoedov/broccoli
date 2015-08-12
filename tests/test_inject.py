
import sample_module

from unittest import TestCase
from injection import bind
from sample_module import *


class TestSample(TestCase):

    def test_bind_no_dependenices(self):
        ok, deps = bind(sample_module.request)
        self.assertFalse(ok)
        self.assertEqual(deps, [])

    def test_bind_should_return_false(self):

        def false_bind(x: type):
            pass
        to_inject = sample_module.new_app()
        ok, deps = bind(false_bind, *to_inject)
        self.assertFalse(ok)
        self.assertEqual(deps, [])

    def test_bind_ok(self):

        to_inject = sample_module.new_app()
        expected = [Db(), Session(), Service()]
        ok, deps = bind(sample_module.request, *to_inject)
        self.assertTrue(ok, deps)
        self.assertEqual(deps, expected)

        try:
            vals = sample_module.request('foo')
        except Exception as e:
            self.fail(e)
        self.assertEqual(vals, ['foo'] + expected)
