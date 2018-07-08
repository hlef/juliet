import unittest, os, tempfile, juliet, filecmp
from juliet.builder import Builder
from juliet import configurator, paths

class builderTest(unittest.TestCase):

    TEST_THEME = "sample_theme"
    DATA_FOLDER = os.path.join("juliet", "tests", "test_data", "source")
    BUILT_FOLDER = os.path.join("juliet", "tests", "test_data", "built")
    DEST_SUBFOLDER = "dest"

    def setUp(self):
        # FIXME this is a big mess
        self.cur_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        self.dest = os.path.join(self.test_dir, self.DEST_SUBFOLDER)

        self.test_data_path = os.path.join(self.cur_dir, self.DATA_FOLDER)
        self.test_built_path = os.path.join(self.cur_dir, self.BUILT_FOLDER)
        self.cfg_local_path = os.path.join(self.DATA_FOLDER, paths.CFG_FILE)
        self.test_cfg_path = os.path.join(self.cur_dir, self.cfg_local_path)

        self.jinja_env = configurator.configure_jinja(self.TEST_THEME, self.test_data_path)
        self.build_args = {"site": configurator.get_config(self.test_cfg_path)}
        args = [self.jinja_env, self.build_args, self.test_data_path, self.dest]

        self.builderclean = Builder(*args, noclean=False)
        self.buildernoclean = Builder(*args, noclean=True)

    def test_build_simple(self):
        """ Make sure that juliet is able to build a simple source correctly. """

        args = juliet.parse_arguments(['build', '--build-src', self.test_data_path,
                                                '--build-dst', self.dest])
        juliet.build(args)
        self.assertTrue(self._dir_trees_identical(self.test_built_path, self.dest))

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

    def _dir_trees_identical(self, dir1, dir2):
        """
        Compare two directories recursively. Files in each directory are
        assumed to be equal if their names and contents are equal.

        @param dir1: First directory path
        @param dir2: Second directory path

        @return: True if the directory trees are the same and
            there were no errors while accessing the directories or files,
            False otherwise.
       """

        dirs_cmp = filecmp.dircmp(dir1, dir2)
        if (len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0
                                        or len(dirs_cmp.funny_files) > 0):
            return False

        (_, mismatch, errors) = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files,
                                                 shallow=False)

        if (len(mismatch) > 0 or len(errors) > 0):
            return False

        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(dir1, common_dir)
            new_dir2 = os.path.join(dir2, common_dir)
            if not self._dir_trees_identical(new_dir1, new_dir2):
                return False

        return True
