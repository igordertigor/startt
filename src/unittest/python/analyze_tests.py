import unittest

from tmpl import analyze


class TestsGetTemplateName(unittest.TestCase):

    def test_html_file_is_html_file(self):
        ext = analyze.get_template_name('ANY_FILE.html')
        self.assertEqual('default.html', ext)

    def test_two_dots_allow_for_versions(self):
        ext = analyze.get_template_name('ANY_FILE.form.html')
        self.assertEqual('form.html', ext)

    def test_dots_in_path_are_ignored(self):
        ext = analyze.get_template_name('ANY_PATH_WITH.DOT/ANY_FILE.html')
        self.assertEqual('default.html', ext)
