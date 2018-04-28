import unittest, shutil, tempfile, juliet, os

class initSiteTest(unittest.TestCase):

    def setUp(self):
        self.cur_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_without_dir(self):
        """ Make sure new article files are well generated with minimal set of
        options. """

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        args = juliet.parse_arguments(['init'])
        juliet.init(args)

        # Test config file
        with open(juliet.paths.CFG_FILE) as f:
            self.assertEqual(f.read(), juliet.defaults.default_config)

        # Test site structure
        for directory in juliet.paths.SOURCE_DIRS:
            self.assertTrue(os.path.isdir(directory))

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_with_dir(self):
        """ Make sure new article files are well generated when date option is
        passed. """

        # Generate base site
        args = juliet.parse_arguments(['init', '--dir', self.test_dir])
        juliet.init(args)

        # Test config file
        cfg_file = os.path.join(self.test_dir, juliet.paths.CFG_FILE)
        with open(cfg_file) as f:
            self.assertEqual(f.read(), juliet.defaults.default_config)

        # Test site structure
        for directory in juliet.paths.SOURCE_DIRS:
            dir_to_check = os.path.join(self.test_dir, directory)
            self.assertTrue(os.path.isdir(dir_to_check))
