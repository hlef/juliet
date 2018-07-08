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

    def test_parse_valid_raw_header_entries(self):
        """ Make sure valid command line passed raw header entries are well parsed. """

        args1 = ["title=", "\"some title\"",
                 "date   ", "=", "\"1997-12-11\"",
                 "author", "=\"The Bird\""]
        res1 = {"title": "some title", "date": "1997-12-11", "author": "The Bird"}
        self.assertEqual(juliet._parse_raw_header_entries(args1), res1)

        args2 = [" title    =", "\"some title with escaped \\\"\"    "]
        res2 = {"title": "some title with escaped \""}
        self.assertEqual(juliet._parse_raw_header_entries(args2), res2)

        args3 = ["title=", "    \"some title with escaped \\\\\""]
        res3 = {"title": "some title with escaped \\"}
        self.assertEqual(juliet._parse_raw_header_entries(args3), res3)

        # Spaces should not be removed between the "s
        args4 = ["title=", "\" some title with escaped \\\\\""]
        res4 = {"title": " some title with escaped \\"}
        self.assertEqual(juliet._parse_raw_header_entries(args4), res4)

    def test_parse_broken_raw_header_entries(self):
        """ Make sure valid command line passed raw header entries are well parsed. """

        # Missing "s
        args1 = ["title=", "some title"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args1)

        # Missing '='
        args2 = ["title", "\"some title\""]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args2)

        # First two combined
        args3 = ["title", "some title"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args3)

        # Only one "
        args4 = ["title=", "\"some title"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args4)

        # Bad key
        args5 = ["_title=", "\"some title\""]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args5)

        # Bad key
        args6 = ["title_=", "\"some title\""]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args6)

        # Bad key
        args7 = ["my title=", "\"some title\""]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args7)

        # String doesn't start directly
        args8 = ["my title=", " something \"some title\""]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args8)

        # Several =s
        args9 = ["my title=", " = \"some title\""]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args9)

        # Missing value
        args10 = ["title="]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args10)

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
        article_path = os.path.join(juliet.paths.POSTS_BUILDDIR, file_name)
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
        self.assertTrue(os.path.exists(article_path),
            "Expected article to be generated at {} but couldn't find it"
            .format(article_path))

        # Make sure it was created at the right place
        self.assertEqual(os.path.dirname(article_path),
                         os.path.join(self.test_dir, juliet.paths.POSTS_PATH),
                             "Expected article to be generated in {} but in fact it was generated at {}"
                             .format(os.path.join(self.test_dir, juliet.paths.POSTS_PATH), os.path.dirname(article_path)))

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_pass_filename(self):
        """ Make sure new article is generated at the right place when file name
        is passed."""

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        b_file_name = 'hello_world.md'
        base_args = ['new', b_file_name]
        comp_args = ['new']
        b_args = juliet.parse_arguments(base_args)
        c_args = juliet.parse_arguments(comp_args)

        # Generate articles
        juliet.init_new_article(b_args)
        juliet.init_new_article(c_args)

        # Make sure article was created where it is expected to be created
        b_article_path = os.path.join(juliet.paths.POSTS_BUILDDIR, b_file_name)

        self.assertTrue(os.path.exists(b_article_path),
            "Expected article to be generated at {} but couldn't find it"
            .format(b_article_path))

        # Make sure it is the same as the default article (passing a file name should only change the file name)
        c_file_name = Template(juliet.defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(juliet.defaults.DEFAULT_THEME_CFG, {}))
        c_article_path = os.path.join(juliet.paths.POSTS_BUILDDIR, c_file_name)

        with open(b_article_path) as b_f:
            with open(c_article_path) as c_f:
                self.assertEqual(b_f.read(), c_f.read(), "passing file name modifies article content")

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_missing_content(self):
        """ Make sure Juliet behaves correctly when folder content is missing. """

        # Do *not* generate base site
        base_args = ['new', '--build-src', self.test_dir]
        args = juliet.parse_arguments(base_args)

        # Try to generate article
        self.assertRaises(FileNotFoundError, juliet.init_new_article, args)
