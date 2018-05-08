import unittest, os, tempfile
from juliet.builder import Builder
from juliet import configurator

class builderTest(unittest.TestCase):

    TEST_THEME = "sample_theme"
    DATA_FOLDER = os.path.join("juliet", "tests", "test_data")
    CFG_FILE = "config.test.yml"
    DEST_SUBFOLDER = "dest"

    def setUp(self):
        self.cur_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        self.dest = os.path.join(self.test_dir, self.DEST_SUBFOLDER)

        self.test_data_path = os.path.join(self.cur_dir, self.DATA_FOLDER)
        self.cfg_local_path = os.path.join(self.DATA_FOLDER, self.CFG_FILE)
        self.test_cfg_path = os.path.join(self.cur_dir, self.cfg_local_path)

        jinja_env = configurator.configure_jinja(self.TEST_THEME, self.test_data_path)
        build_args = configurator.get_config(self.test_cfg_path)
        args = [jinja_env, build_args, self.test_data_path, self.dest]

        self.builderclean = Builder(*args, False)
        self.buildernoclean = Builder(*args, True)

    def test_write(self):
        """ Make sure that the internal write function is working well with
        simple tasks. """

        # simple file
        path1 = os.path.join(self.dest, "test_string1")
        string1 = "This is a string."

        # simple file in subfolder
        path2 = os.path.join(self.dest, "subfolder", "test_string2")
        string2 = string1

        # simple file in multiple subfolders
        path3 = os.path.join(self.dest, "sub1", "sub2", "test_string3")
        string3 = string1

        strings = { string1: path1, string2: path2, string3: path3 }

        for string, path in strings.items():
            self.builderclean._write(path, string)
            with open(path) as f:
                self.assertEqual(f.read(), string)

            # cleanup before testing with noclean
            os.remove(path)

            self.buildernoclean._write(path, string)
            with open(path) as f:
                self.assertEqual(f.read(), string)
