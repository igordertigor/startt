from unittest import TestCase
from unittest import mock

from startt import config


class TestConfig(TestCase):

    def setUp(self):
        self.patches = {
            'exists': mock.patch('startt.config.os.path.exists'),
            'open': mock.patch('startt.config.open',
                               new_callable=mock.mock_open),
            'json_load': mock.patch('startt.config.json.load'),
        }
        self.mocks = {
            name: patch.start() for name, patch in self.patches.items()
        }

    def tearDown(self):
        mock.patch.stopall()

    def test_default_is_link(self):
        self.mocks['exists'].return_value = False
        cfg = config.config('ANY_PATH')
        self.assertDictEqual({'default': 'link'}, cfg)

    def test_default_is_set_if_read_from_file(self):
        self.mocks['exists'].return_value = True
        self.mocks['json_load'].return_value = {}

        cfg = config.config('ANY_PATH')
        self.assertIn('default', cfg)
        self.assertEqual(cfg['default'], 'link')

    def test_default_can_be_overwritten_from_file(self):
        self.mocks['exists'].return_value = True
        self.mocks['json_load'].return_value = {'default': 'copy'}

        cfg = config.config('ANY_PATH')
        self.assertIn('default', cfg)
        self.assertEqual(cfg['default'], 'copy')

    def test_filename_is_relative_to_project_path(self):
        self.mocks['exists'].return_value = False
        config.config('ANY_PATH')
        self.mocks['exists'].assert_called_once_with('ANY_PATH/config.json')

    def test_other_filenames_can_be_specified_separately(self):
        self.mocks['exists'].return_value = True
        self.mocks['json_load'].return_value = {'file.py': 'copy',
                                                'other_file.txt': 'link'}
        cfg = config.config('ANY_PATH')
        self.assertDictEqual(cfg, {'default': 'link',
                                   'ANY_PATH/file.py': 'copy',
                                   'ANY_PATH/other_file.txt': 'link'})

    def test_fail_if_invalid_transfer_options(self):
        self.mocks['exists'].return_value = True
        self.mocks['json_load'].return_value = {'file.py': 'invalid'}
        with self.assertRaises(ValueError):
            config.config('ANY_PATH')
