"""Unit tests for utils module."""

import unittest

from mainspring import utils


class UtilsTest(unittest.TestCase):

    def test_class_import_from_path(self):
        path = 'mainspring.default_settings_test'
        module = utils.import_from_path(path)
        self.assertEqual(module.DEBUG, True)
