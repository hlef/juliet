import unittest, shutil, tempfile, juliet, os, datetime
from string import Template
from juliet.pageprocessor import PageProcessor
from juliet import defaults

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
        """ Make sure valid command line passed raw header entries are well
        parsed. """

        args_standard = ["--", "title:", "a title", "date:", "1997-12-11", "author:", "Bird"]
        parsed_standard = {"title": "a title", "date": "1997-12-11", "author": "Bird"}
        self.assertEqual(juliet._parse_raw_header_entries(args_standard), parsed_standard)

        args_no_colon = ["--", "title", "a title"]
        parsed_no_colon = {"title": "a title"}
        self.assertEqual(juliet._parse_raw_header_entries(args_no_colon), parsed_no_colon)

    def test_parse_broken_raw_header_entries(self):
        """ Make sure valid command line passed raw header entries are well
        parsed. """

        # Missing value
        args_missing_value = ["--", "title"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args_missing_value)

        # Invalid key #1
        args_invalid_key = ["--", "::", "hello"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args_invalid_key)

        # Invalid key #2
        args_invalid_key = ["--", "title_of_the_death:", "hello"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args_invalid_key)

        # Invalid key #3 (empty key)
        args_empty_key = ["--", ":", "title"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args_empty_key)

        # Shifted colon (last key missing value!)
        args_shifted_colon = ["--", "title", ":", "a title"]
        self.assertRaises(ValueError, juliet._parse_raw_header_entries, args_shifted_colon)

    def test_generate_default(self):
        """ Make sure new article files are generated. Check for default content. """

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
        filename = Template(defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(defaults.DEFAULT_THEME_CFG, {}))
        path = os.path.join(juliet.paths.POSTS_BUILDDIR, filename)
        self.assertTrue(os.path.exists(path),
            "Expected article to be generated at {} but couldn't find it"
            .format(path))

        # Retrieve and parse generated header
        raw_file = ""
        with open(path) as f:
            raw_file = f.read()

        parsed_header = PageProcessor._get_parsed_header(raw_file, filename,
                            defaults.DEFAULT_FILE_NAMING_VARIABLE)

        for key, value in defaults.DEFAULT_THEME_CFG.items():
            if (value[1] != None):
                self.assertTrue(parsed_header[key] == value[1])
            elif (key == "date"):
                # We did not pass date, so expect it to be the current day
                self.assertEqual(parsed_header[key], datetime.date.today())

        # Go back to current directory
        os.chdir(self.cur_dir)

    def _test_generate_with_remainder(self, remainder):
        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        base_args = ['new', *remainder]
        args = juliet.parse_arguments(base_args)
        parsed_header_entries = juliet._parse_raw_header_entries(remainder)

        # Generate article
        juliet.init_new_article(args)

        # Make sure article was created
        filename = Template(defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(defaults.DEFAULT_THEME_CFG, parsed_header_entries))
        path = os.path.join(juliet.paths.POSTS_BUILDDIR, filename)
        self.assertTrue(os.path.exists(path),
            "Expected article to be generated at {} but couldn't find it"
            .format(path))

        # Retrieve and parse generated header
        raw_file = ""
        with open(path) as f:
            raw_file = f.read()

        parsed_header = PageProcessor._get_parsed_header(raw_file, filename,
                            defaults.DEFAULT_FILE_NAMING_VARIABLE)

        for key, value in parsed_header_entries.items():
            self.assertTrue(parsed_header[key] == value)

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_generate_with_remainder(self):
        """ Make sure new article files are generated correctly when a remainder
        is passed. """

        self._test_generate_with_remainder(['--', 'title', 'hello world'])
        self._test_generate_with_remainder(['--', 'author', 'M. John Hacker'])
        self._test_generate_with_remainder(['--', 'city', 'Karlsruhe'])
        self._test_generate_with_remainder(['--', 'joking', 'False'])

    def test_generate_default_with_dest_folder(self):
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
        file_name = Template(defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(defaults.DEFAULT_THEME_CFG, {}))
        article_path = os.path.join(args.src, juliet.paths.POSTS_BUILDDIR, file_name)
        self.assertTrue(os.path.exists(article_path),
            "Expected article to be generated at {} but couldn't find it"
            .format(article_path))

        # Make sure it was created at the right place
        self.assertEqual(os.path.dirname(article_path),
                         os.path.join(self.test_dir, juliet.paths.POSTS_PATH),
                             "Expected article to be generated in {} but in fact it was generated at {}"
                             .format(os.path.join(self.test_dir, juliet.paths.POSTS_PATH), os.path.dirname(article_path)))

    def test_generate_default_with_filenaming_pattern(self):
        """ Make sure new article files are generated with the right name when a
        filenaming pattern is specified. Doesn't check for content. """

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Add filenaming pattern
        with open(juliet.paths.CFG_FILE, "a") as cfgfile:
            cfgfile.write("filenaming_pattern: 'article-$number.md'")

        # Prepare args
        base_args = ['new', '--', 'number', '12']
        args = juliet.parse_arguments(base_args)

        # Generate article
        juliet.init_new_article(args)

        # Make sure article was created
        file_name = "article-12.md"
        article_path = os.path.join(juliet.paths.POSTS_BUILDDIR, file_name)
        self.assertTrue(os.path.exists(article_path),
            "Expected article to be generated at {} but couldn't find it"
            .format(article_path))

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_missing_structure(self):
        """ Make sure Juliet behaves correctly when folder content is missing. """

        # Do *not* generate base site
        base_args = ['new', '--build-src', self.test_dir]
        args = juliet.parse_arguments(base_args)

        # Try to generate article
        self.assertRaises(FileNotFoundError, juliet.init_new_article, args)

    def test_pass_filename(self):
        """ Make sure new article is generated at the right place when file name
        is passed. Make sure that passing a file name does not modify the actual
        content."""

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        b_file_name = 'hello_world.md'
        base_args = ['new', '-f', b_file_name]
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
        c_file_name = Template(defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(juliet._process_header_dict(defaults.DEFAULT_THEME_CFG, {}))
        c_article_path = os.path.join(juliet.paths.POSTS_BUILDDIR, c_file_name)

        with open(b_article_path) as b_f:
            with open(c_article_path) as c_f:
                self.assertEqual(b_f.read(), c_f.read(), "passing file name modifies article content")

        # Go back to current directory
        os.chdir(self.cur_dir)

    def test_pass_filename_and_remainder(self):
        """ Make sure new article files are generated when a destination folder
        is specified together with a remainder (-- stuff). Doesn't check for
        content. """

        # Go to temporary directory
        os.chdir(self.test_dir)

        # Generate base site
        self._init_juliet_structure_in_test_dir()

        # Prepare args
        file_name = 'my-new-article.md'
        base_args = ['new', '-f', file_name, '--', 'title', 'value']
        args = juliet.parse_arguments(base_args)

        # Generate article
        juliet.init_new_article(args)

        # Make sure article was created
        article_path = os.path.join(juliet.paths.POSTS_BUILDDIR, file_name)
        self.assertTrue(os.path.exists(article_path),
            "Expected article to be generated at {} but couldn't find it"
            .format(article_path))

        # Go back to current directory
        os.chdir(self.cur_dir)
