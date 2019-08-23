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
            'glob': mock.patch('startt.process.glob.glob'),
            'copyfile': mock.patch('startt.process.copyfile'),
            'symlink': mock.patch('startt.process.os.symlink'),
            'config': mock.patch('startt.process.config.config'),
        }
        self.mocks = {
            name: patch.start()
            for name, patch in self.patches.items()
        }
        self.mocks['config'].return_value = {'default': 'link'}

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

    def test_respects_default_operation_setting(self):
        self.mocks['config'].return_value = {'default': 'copy'}
        self.mocks['glob'].return_value = ['ANY_TEMPLATE/ANY_FILE.ext']
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_NEW_NAME.ext')
        self.mocks['symlink'].assert_not_called()
        self.mocks['copyfile'].assert_called_once_with(
            'ANY_TEMPLATE/ANY_FILE.ext',
            'ANY_FILE.ext')

    def test_gets_config_for_directory(self):
        self.mocks['glob'].return_value = []
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_NAME.ext')
        self.mocks['config'].assert_called_once_with('ANY_TEMPLATE')

    def test_respects_per_file_setting(self):
        self.mocks['config'].return_value = {
            'default': 'link',
            'ANY_TEMPLATE/ANY_FILE.ext': 'copy',
        }
        self.mocks['glob'].return_value = ['ANY_TEMPLATE/ANY_FILE.ext',
                                           'ANY_TEMPLATE/OTHER_FILE.ext']
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_NEW_NAME.ext')
        self.mocks['symlink'].assert_called_once_with(
            'ANY_TEMPLATE/OTHER_FILE.ext',
            'OTHER_FILE.ext')
        self.mocks['copyfile'].assert_called_once_with(
            'ANY_TEMPLATE/ANY_FILE.ext',
            'ANY_FILE.ext')

    def test_dont_copy_config_file(self):
        self.mocks['glob'].return_value = ['ANY_TEMPLATE/ANY_FILE.ext',
                                           'ANY_TEMPLATE/config.json']
        process.copy_directory_template('ANY_TEMPLATE', 'ANY_NEW_NAME.ext')
        self.mocks['symlink'].assert_called_once_with(
            'ANY_TEMPLATE/ANY_FILE.ext',
            'ANY_FILE.ext')


class TestsCopyTemplate(unittest.TestCase):

    @mock.patch('startt.process.os.path.isfile')
    @mock.patch('startt.process.copy_file_template')
    def test_copies_single_file(self, mock_copy_file, mock_isfile):
        mock_isfile.return_value = True
        process.copy_template('ANY_FILE.ext', 'ANY_FOLDER/')
        mock_copy_file.assert_called_once_with(
            'ANY_FOLDER/default.ext', 'ANY_FILE.ext')

    @mock.patch('startt.process.os.path.isfile')
    @mock.patch('startt.process.os.path.isdir')
    @mock.patch('startt.process.copy_directory_template')
    def test_directory_match_copies_folder(self,
                                           mock_copy_dir,
                                           mock_isdir,
                                           mock_isfile):
        mock_isfile.return_value = False
        mock_isdir.return_value = True
        process.copy_template('ANY_FILE.ext', 'ANY_FOLDER/')
        mock_copy_dir.assert_called_once_with(
            'ANY_FOLDER/default.ext', 'ANY_FILE.ext')
