import unittest, shutil, tempfile, juliet, os

class newArticleFileTest(unittest.TestCase):

    def setUp(self):
        self.cur_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _init_juliet_structure_in_test_dir(self):
        args = juliet.parse_arguments(['init', '--dir', self.test_dir])
        juliet.init(args)

    def test_generate(self):
        """ Make sure new article files are well generated with minimal set of options. """

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        base_args = ['new', '--title', '"Test article"']
        args1 = juliet.parse_arguments(base_args)
        args2 = juliet.parse_arguments(base_args + ['--date', '1970-01-01'])
        args3 = juliet.parse_arguments(base_args + ['--date', '9999-12-12'])

        for args in [args1, args2, args3]:
            # Generate article
            juliet.init_new_article(args)

            # Make sure article was created and contains expected content
            article_path = juliet._get_article_path(args)
            with open(article_path) as f:
                self.assertEqual(f.read(), juliet._get_default_article(args))

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_with_dest_folder(self):
        """ Make sure new article files are well generated when a destination folder is specified. """

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        base_args = ['new', '--title', '"Test article"', '--build-src', self.test_dir]
        args1 = juliet.parse_arguments(base_args)
        args2 = juliet.parse_arguments(base_args + ['--date', '1970-01-01'])
        args3 = juliet.parse_arguments(base_args + ['--date', '9999-12-12'])

        for args in [args1, args2, args3]:
            # Generate article
            juliet.init_new_article(args)

            # Make sure article was created and contains expected content
            article_path = juliet._get_article_path(args)
            with open(article_path) as f:
                self.assertEqual(f.read(), juliet._get_default_article(args))

    def test_invalid_date(self):
        """ Make sure date parsing is correct. """

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare invalid args
        base_args = ['new', '--title', '"Test article"', '--build-src', self.test_dir]
        args1 = base_args + ['--date']
        args2 = args1 + ['01-01']
        args3 = args1 + ['hello']

        # Make sure Juliet exits when it encouters them
        for args in [args1, args2, args3]:
            with self.assertRaises(SystemExit):
                juliet.parse_arguments(args)

    def test_missing_posts_folder(self):
        """ Make sure Juliet behaves correctly when posts folder is missing. """

        # Do *not* generate base site
        base_args = ['new', '--title', '"Test article"', '--build-src', self.test_dir]
        args1 = juliet.parse_arguments(base_args)
        args2 = juliet.parse_arguments(base_args + ['--date', '1970-01-01'])
        args3 = juliet.parse_arguments(base_args + ['--date', '9999-12-12'])

        # Try to generate article
        for args in [args1, args2, args3]:
            self.assertRaises(FileNotFoundError, juliet.init_new_article, args)
