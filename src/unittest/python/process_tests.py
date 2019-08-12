import unittest
from unittest import mock

from tmpl import process


class TestsGetFilename(unittest.TestCase):

    def test_default_filename_is_unchanged(self):
        new_fname = process.get_filename('ANY_NAME.ext')
        self.assertEqual('ANY_NAME.ext', new_fname)

    def test_version_specifier_is_ignored(self):
        new_fname = process.get_filename('ANY_NAME.letter.ext')
        self.assertEqual('ANY_NAME.ext', new_fname)

    def test_foldername_is_respected(self):
        new_fname = process.get_filename('ANY.FOLDER.WITH.DOTS/ANY_NAME.ext')
        self.assertEqual('ANY.FOLDER.WITH.DOTS/ANY_NAME.ext', new_fname)
