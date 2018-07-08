import unittest, os, tempfile
from juliet.builder import Builder
from juliet import configurator, paths

class builderTest(unittest.TestCase):

    TEST_THEME = "sample_theme"
    DATA_FOLDER = os.path.join("juliet", "tests", "test_data", "source")
    DEST_SUBFOLDER = "dest"

    def setUp(self):
        self.cur_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        self.dest = os.path.join(self.test_dir, self.DEST_SUBFOLDER)

        self.test_data_path = os.path.join(self.cur_dir, self.DATA_FOLDER)
        self.cfg_local_path = os.path.join(self.DATA_FOLDER, paths.CFG_FILE)
        self.test_cfg_path = os.path.join(self.cur_dir, self.cfg_local_path)

        self.jinja_env = configurator.configure_jinja(self.TEST_THEME, self.test_data_path)
        self.build_args = configurator.get_config(self.test_cfg_path)
        args = [self.jinja_env, self.build_args, self.test_data_path, self.dest]

        self.builderclean = Builder(*args, noclean=False)
        self.buildernoclean = Builder(*args, noclean=True)

    def test_build_simple(self):
        # TODO: test no assets / no statics folder
        raise NotImplementedError()

    def test_is_safe_path(self):
        """ Make sure that the is_safe_path function acts as excepted when valid
        and invalid (out of tree, etc.) paths. """

        v_path1 = os.path.join(self.dest, "file")
        v_path2 = os.path.join(self.dest, "subfolder", "file")
        v_path3 = os.path.join(self.dest, "subfolder", "subfolder", "file")
        valids = [v_path1, v_path2, v_path3]

        for path in valids:
            self.assertTrue(self.builderclean._is_safe_path(path))
            self.assertTrue(self.buildernoclean._is_safe_path(path))

        inv_path1 = os.path.join(self.dest, "..", "file")
        inv_path2 = os.path.join("etc", "apache2")
        inv_path3 = os.path.join(self.dest, "..", "..", "..", "file")
        inv_path4 = ""
        invalids = [inv_path1, inv_path2, inv_path3, inv_path4]

        for path in invalids:
            self.assertFalse(self.builderclean._is_safe_path(path))
            self.assertFalse(self.buildernoclean._is_safe_path(path))

    def test_is_safe_path_with_relative_paths(self):
        """ Make sure that is_safe_path behaves well when it is passed relative
        paths."""

        relative_path = os.path.join("..", "whatever")
        args = [self.jinja_env, self.build_args, self.test_data_path, relative_path]
        builderrelative = Builder(*args, noclean=False)

        path = os.path.join(relative_path, "hello")
        self.assertTrue(builderrelative._is_safe_path(path))

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
