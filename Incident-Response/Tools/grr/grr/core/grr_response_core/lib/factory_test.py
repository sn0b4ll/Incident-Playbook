#!/usr/bin/env python
from typing import Text

from absl.testing import absltest

from grr_response_core.lib import factory


class FactoryTest(absltest.TestCase):

  def testRegisterAndUnregister(self):
    del self  # Unused.

    obj_factory = factory.Factory(object)

    # First, we check whether registering works.
    obj_factory.Register("foo", object)
    obj_factory.Register("bar", object)

    # Now, we should be able to unregister these constructors.
    obj_factory.Unregister("foo")
    obj_factory.Unregister("bar")

    # Once they are unregistered, names are free to be bound again.
    obj_factory.Register("foo", object)
    obj_factory.Register("bar", object)

  def testRegisterDuplicateThrows(self):
    obj_factory = factory.Factory(object)
    obj_factory.Register("foo", object)
    obj_factory.Register("bar", object)

    with self.assertRaisesRegex(ValueError, "foo"):
      obj_factory.Register("foo", object)

  def testUnregisterThrowsForUnknown(self):
    obj_factory = factory.Factory(object)

    with self.assertRaisesRegex(ValueError, "foo"):
      obj_factory.Unregister("foo")

  def testCreateString(self):
    str_factory = factory.Factory(Text)
    str_factory.Register("foo", Text, lambda: "FOO")
    str_factory.Register("bar", Text, lambda: "BAR")
    str_factory.Register("baz", Text, lambda: "BAZ")

    self.assertEqual(str_factory.Create("foo"), "FOO")
    self.assertEqual(str_factory.Create("bar"), "BAR")
    self.assertEqual(str_factory.Create("baz"), "BAZ")

  def testUsesClassConstructor(self):
    str_factory = factory.Factory(str)
    str_factory.Register("foo", str)
    self.assertEqual(str_factory.Create("foo"), "")

  def testCreateClass(self):

    class Foo(object):
      pass

    class Bar(object):
      pass

    cls_factory = factory.Factory(object)
    cls_factory.Register("Foo", Foo)
    cls_factory.Register("Bar", Bar)

    self.assertIsInstance(cls_factory.Create("Foo"), Foo)
    self.assertIsInstance(cls_factory.Create("Bar"), Bar)

  def testCreateUnregisteredThrows(self):
    int_factory = factory.Factory(int)

    with self.assertRaisesRegex(ValueError, "foo"):
      int_factory.Create("foo")

  def testGetAllTypesWithoutResults(self):
    obj_factory = factory.Factory(object)

    self.assertCountEqual(list(obj_factory.GetTypes()), [])

  def testGetTypesReturnsAllTypes(self):

    class Foo(object):
      pass

    class Bar(object):
      pass

    int_factory = factory.Factory(object)
    int_factory.Register("foo", Foo)
    int_factory.Register("bar", Bar)

    self.assertCountEqual(list(int_factory.GetTypes()), [Foo, Bar])


if __name__ == "__main__":
  absltest.main()
