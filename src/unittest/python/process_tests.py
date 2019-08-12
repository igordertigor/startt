import unittest
from unittest import mock

from startt import process


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


class TestCopyDirectoryTemplate(unittest.TestCase):

    def setUp(self):
        self.patches = {
            'glob': mock.patch('tmpl.process.glob.glob'),
            'copyfile': mock.patch('tmpl.process.copyfile'),
            'symlink': mock.patch('tmpl.process.os.symlink'),
        }
        self.mocks = {
            name: patch.start()
            for name, patch in self.patches.items()
        }

    def tearDown(self):
        for name, patch in self.patches.items():
            patch.stop()

    def test_calls_glob_to_get_template_content(self):
        self.mocks['glob'].return_value = []
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_TARGET.ext')
        self.mocks['glob'].assert_called_once_with('ANY_TEMPLATE/*')

    def test_symlinks_for_normal_files(self):
        self.mocks['glob'].return_value = ['ANY_TEMPLATE/ANY_FILE.ext']
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_TARGET.ext')
        self.mocks['symlink'].assert_called_once_with(
            'ANY_TEMPLATE/ANY_FILE.ext',
            'ANY_FILE.ext')
        self.mocks['copyfile'].assert_not_called()

    def test_copies_main_file(self):
        self.mocks['glob'].return_value = ['ANY_TEMPLATE/main_ANY_FILE.ext']
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_NEW_NAME.ext')
        self.mocks['copyfile'].assert_called_once_with(
            'ANY_TEMPLATE/main_ANY_FILE.ext',
            'ANY_NEW_NAME.ext')
        self.mocks['symlink'].assert_not_called()

    def test_handles_all_files(self):
        self.mocks['glob'].return_value = [
            'ANY_TEMPLATE/main_ANY_FILE.ext',
            'ANY_TEMPLATE/ANY_OTHER_FILE.ext',
        ]
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_NEW_NAME.ext')
        self.mocks['copyfile'].assert_called_once_with(
            'ANY_TEMPLATE/main_ANY_FILE.ext',
            'ANY_NEW_NAME.ext')
        self.mocks['symlink'].assert_called_once_with(
            'ANY_TEMPLATE/ANY_OTHER_FILE.ext',
            'ANY_OTHER_FILE.ext')
