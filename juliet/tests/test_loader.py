import unittest, shutil, tempfile, juliet, os

class loaderTest(unittest.TestCase):

    def setUp(self):
        self.cur_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()

    def test_load_articles(self):
        """ Make sure that all articles are loaded as expected. """

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        args = juliet.parse_arguments(['init'])
        juliet.init(args)

        # Generate a few articles
        args = juliet.parse_arguments(['new', '--', 'title', 'Hello, World!'])
        juliet.init_new_entry(args)
        args = juliet.parse_arguments(['new', '--', 'title', 'First article'])
        juliet.init_new_entry(args)
        args = juliet.parse_arguments(['new', '--', 'title', 'Trip to France'])
        juliet.init_new_entry(args)

        # Make sure are articles can be loaded as expected
        config = {"site": juliet.configurator.get_config(juliet.paths.CFG_FILE)}
        posts = juliet.loader.get_from_folder(juliet.paths.POSTS_PATH, config)

        self.assertEqual(len(posts), 3)

        # Go back to current directory
        os.chdir(self.cur_dir)

