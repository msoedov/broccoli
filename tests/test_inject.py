import sample_module

from unittest import TestCase
from injection import bind
from sample_module import *


class TestSample(TestCase):
    def setUp(self):
        self.to_inject = new_app()

    def test_bind_no_dependenices(self):
        ok, deps = bind(sample_module.request)
        self.assertFalse(ok)
        self.assertEqual(deps, [])

    def test_bind_should_return_false(self):
        def false_bind(x: type):
            pass

        ok, deps = bind(false_bind, *self.to_inject)
        self.assertFalse(ok)
        self.assertEqual(deps, [])

    def test_bind_ok(self):

        expected = [Db(), Session(), Service()]
        ok, deps = bind(request, *self.to_inject)
        self.assertTrue(ok, deps)
        self.assertEqual(deps, expected)

        try:
            vals = request('foo')
        except Exception as e:
            self.fail(e)
        self.assertSequenceEqual(vals, ['foo'] + expected)

    def test_do_stuff(self):

        with self.assertRaises(TypeError):
            bind(do_stuff, *self.to_inject)

    def test_validation(self):
        expected = [Session()]
        ok, deps = bind(validation, *self.to_inject)
        self.assertTrue(ok, deps)
        self.assertEqual(deps, expected)

        vals = validation('bar')

        self.assertSequenceEqual(vals, ['bar'] + expected)
