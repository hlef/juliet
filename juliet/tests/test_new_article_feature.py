import unittest, shutil, tempfile, juliet, os
from string import Template

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
        """ Make sure new article files are generated. Doesn't check for content. """

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        base_args = ['new']
        args = juliet.parse_arguments(base_args)

        # Generate article
        juliet.init_new_article(args)

        # Make sure article was created
        file_name = Template(juliet.defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(juliet.defaults.DEFAULT_THEME_CFG, {}))
        article_path = os.path.join(args.src, juliet.paths.POSTS_BUILDDIR, file_name)
        self.assertTrue(os.path.exists(article_path),
            "Expected article to be generated at {} but couldn't find it"
            .format(article_path))

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_with_dest_folder(self):
        """ Make sure new article files are generated when a destination folder
        is specified. Doesn't check for content. """

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        base_args = ['new', '--build-src', self.test_dir]
        args = juliet.parse_arguments(base_args)

        # Generate article
        juliet.init_new_article(args)

        # Make sure article was created
        file_name = Template(juliet.defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(juliet.defaults.DEFAULT_THEME_CFG, {}))
        article_path = os.path.join(args.src, juliet.paths.POSTS_BUILDDIR, file_name)
        self.assertTrue(os.path.exists(article_path))

        # Make sure it was created at the right place
        self.assertEqual(os.path.dirname(article_path),
                         os.path.join(self.test_dir, juliet.paths.POSTS_PATH))

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_missing_posts_folder(self):
        """ Make sure Juliet behaves correctly when folder content is missing. """

        # Do *not* generate base site
        base_args = ['new', '--build-src', self.test_dir]
        args = juliet.parse_arguments(base_args)

        # Try to generate article
        self.assertRaises(FileNotFoundError, juliet.init_new_article, args)
