from unittest import TestCase
from broccoli import bind
from .fixtures.test_module import *


class TestBind(TestCase):

    def setUp(self):
        self.to_inject = new_app()

    def test_bind_no_dependenices(self):
        ok, deps = bind(request)
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

    def test_class(self):
        ok, deps = bind(Foo.__init__, *self.to_inject)
        self.assertTrue(ok)
        self.assertIn(Foo().db, self.to_inject)

    def test_single_argument(self):
        expected = Db()
        ok, deps = bind(update_query, *self.to_inject)
        self.assertTrue(ok, deps)
        self.assertEqual(deps, [expected])

        try:
            vals = update_query()
        except Exception as e:
            self.fail(e)
        self.assertEqual(vals, expected)
