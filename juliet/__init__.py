import shutil, zipfile, argparse, yaml, logging, os, slugify, datetime, dateutil.parser, sys
from juliet import configurator, loader, paths, defaults, version
from juliet.builder import Builder
from pkg_resources import resource_filename
from string import Template

def main():
    """ Parse command line arguments and execute passed subcommands. """

    args = parse_arguments(sys.argv[1:])
    configure_logging(args.debug)

    if(args.subcommand):
        logging.debug("Executing sub-command " + args.subcommand)

    if(args.subcommand == "build"):
        build(args)
    elif(args.subcommand == "init"):
        init(args)
    elif(args.subcommand == "new"):
        init_new_article(args, args.buildpage)

    logging.debug("Done. Exiting.")

def build(args):
    """ Build website to configured location. """

    logging.info("Parsing configuration...")
    try:
        config = {"site": configurator.get_config(os.path.join(args.src, args.configfile))}
    except Exception as exc:
        sys.exit("Error during configuration: " + str(exc))

    if (args.autobaseurl):
        config["site"]["baseurl"] = os.path.abspath(args.dest)

    logging.info("Loading and pre-processing content...")
    if (os.path.isdir(os.path.join(args.src, paths.POSTS_PATH))):
        try:
            config["posts"] = loader.get_from_folder(os.path.join(args.src, paths.POSTS_PATH), config)
        except ValueError as exc:
            sys.exit("Error loading posts: " + str(exc))
    else:
        config["posts"] = {}

    if (os.path.isdir(os.path.join(args.src, paths.PAGES_PATH))):
        try:
            config["pages"] = loader.get_from_folder(os.path.join(args.src, paths.PAGES_PATH), config)
        except ValueError as exc:
            sys.exit("Error loading pages: " + str(exc))
    else:
        config["pages"] = {}

    logging.debug("Configuring Jinja2 environment...")
    jinjaEnv = configurator.configure_jinja(config["site"]["theme"], args.src)

    logging.debug("Initializing builder...")
    Builder(jinjaEnv, config, args.src, args.dest, args.noclean).build()

def init(args):
    """ Initialize a new, clean website in passed directory."""

    logging.debug("Creating source directories")
    for directory in paths.SOURCE_DIRS:
        os.makedirs(os.path.join(args.dir, directory), exist_ok=True)

    logging.debug("Installing default theme")
    default_theme_path = os.path.join(args.dir, paths.THEMES_PATH, defaults.DEFAULT_THEME_NAME)
    os.makedirs(default_theme_path, exist_ok=True)
    with zipfile.ZipFile(resource_filename(__name__, "resources/" +
                         defaults.DEFAULT_THEME_NAME + ".zip")) as zipped_theme:
        zipped_theme.extractall(path=default_theme_path)

    logging.debug("Importing default config file")
    shutil.copyfile(os.path.join(default_theme_path, paths.EXAMPLE_CFG_FILE),
                    os.path.join(args.dir, paths.CFG_FILE))

def parse_arguments(args):
    """ Parse and return arguments. """

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--debug', '-d', action='count', default=0)
    parent_parser.add_argument('--version', '-v', action='version',
                       version='%(prog)s {version}'.format(version=version.__version__))

    main_parser = argparse.ArgumentParser(parents=[parent_parser],
                        description='The lightweight static website generator')

    subparsers = main_parser.add_subparsers(help="sub-command to be executed",
                                            dest="subcommand")
    subparsers.required = True

    parser_build = subparsers.add_parser('build', parents=[parent_parser],
    help="Build static site from local directory to the directory specified in config.yml")

    parser_build.add_argument('--build-src', '-s', dest="src", type=str, default="",
                    help='directory to load source')

    parser_build.add_argument('--build-dst', '-ds', dest="dest", type=str,
                    default=paths.DEFAULT_BUILDDIR,
                    help='build and install website in passed directory')

    parser_build.add_argument('--no-clean', '-nc', dest="noclean",
                    default=False, action='store_true',
                    help='do not clean build directory before installation')

    parser_build.add_argument('--config-file', '-cf', dest="configfile",
                    default=paths.CFG_FILE, type=str,
                    help='use a non default config file')

    parser_build.add_argument('--auto-baseurl', dest="autobaseurl",
                    default=False, action='store_true',
                    help='override baseurl and set it to build destination (useful for local builds)')

    parser_init = subparsers.add_parser('init', parents=[parent_parser],
    help="Initialize a new, clean website in current directory.")

    parser_init.add_argument('--dir', dest="dir", type=str,
                    default=paths.DEFAULT_INITDIR,
                    help='Initialize website in passed directory')

    parser_new = subparsers.add_parser('new', parents=[parent_parser],
    help="Initialize a fresh, new article file.")

    parser_new.add_argument('--build-src', '-s', dest="src", type=str, default="",
                    help='juliet source directory where to initialize post/page')

    parser_new.add_argument('--file-name', '-f', dest="file_name", nargs='?',
                            default=None, help='file name for new post/page')

    parser_new.add_argument('--page', dest="buildpage", default=False, action='store_true',
                            help='build a new page (instead of a new post)')

    parser_new.add_argument('header_content', default=[],
    nargs=argparse.REMAINDER, help='header content of the new article')

    return main_parser.parse_args(args)

def _parse_raw_header_entries(header_entries):
    """ Parse header entries passed by the user as command line argument. """

    def __check_key(key):
        return not("_" in key or " " in key or ":" in key or not len(key))

    result = {}
    if (len(header_entries) < 1):
        return result

    # Remove leading '--'
    header_entries = header_entries[1:]
    if (not len(header_entries) % 2 == 0):
        raise ValueError("last key does not have a value")

    while (len(header_entries)):
        # Retrieve raw key
        logging.debug("current header content " + str(header_entries))
        word = header_entries[0]
        header_entries = header_entries[1:]

        # Try to trim equal
        if (word[-1] == ':'):
            word = word[:-1]

        if(not __check_key(word)):
            raise ValueError("invalid key '{}' in key value list".format(word))

        result[word] = header_entries[0]
        header_entries = header_entries[1:]

    return result

def _get_article_path(args, user_config, processed_entries, page=False):
    """ Return article path matching passed args. """

    article_filename = ""
    if (not page):
        if (args.file_name):
            article_filename = args.file_name
        elif ("filenaming_pattern" in user_config.keys()):
            article_filename = Template(user_config["filenaming_pattern"]).substitute(**processed_entries)
        else:
            article_filename = Template(defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(**processed_entries)
    else:
        article_filename = Template(defaults.DEFAULT_PAGE_NAMING_PATTERN).substitute(**processed_entries)

    if (not page):
        final_path = os.path.join(args.src, paths.POSTS_BUILDDIR, article_filename)
    else:
        final_path = os.path.join(args.src, paths.PAGES_BUILDDIR, article_filename)

    if os.path.exists(final_path):
        raise ValueError("can't create new article at " + final_path + ": file already does already exist")

    return final_path

def _process_header_dict(theme_headers, raw_entries):
    """ TODO """

    entries = _parse_raw_header_entries(raw_entries)

    for key, value in theme_headers.items():
        if (key not in entries.keys() and value):
            # Fix missing entries with theme's defaults
            entries[key] = value
        elif (key == "date"):
            if (key in entries.keys()):
                try:
                    entries["date_"] = entries[key] = dateutil.parser.parse(entries[key]).date()
                except (ValueError, OverflowError):
                    pass

    # Apply modifiers
    result = entries.copy()
    for key, value in entries.items():
        if(isinstance(value, str)):
            result["slug_" + key] = slugify.slugify(value)

    # Generate date_ if not already in result
    if ("date_" not in result.keys()):
        result["date_"] = datetime.date.today()
        if ("date" in theme_headers.keys()):
            # this happens when dateutil.parser.parse failed
            # or 'date' was not in entries
            result["date"] = result["date_"]

    return result

def init_new_article(args, page=False):
    """ Initialize a fresh, new post/page file. """

    buildingfor = "posts"
    if (page):
        buildingfor = "pages"

    def _remove_temporary_entries(entries):
        result = {}
        for key, value in processed_entries.items():
            if (not "_" in key):
                result[key] = value

        return result

    def _get_new_article(final_header):
        default_article = "---\n" + yaml.dump(final_header, allow_unicode=True,
            default_flow_style=False) + "---"
        return default_article

    # Get configs
    user_config = configurator.get_config(os.path.join(args.src, paths.CFG_FILE))
    if (not user_config):
        logging.error("Error, could not find user config at {}".format(
            os.path.join(args.src, paths.CFG_FILE)))
        return

    theme_headers = defaults.DEFAULT_THEME_HEADERS
    theme_headers_file = os.path.join(args.src, paths.THEMES_PATH,
        user_config["theme"], paths.THEME_HEADERS_FILE)
    if (os.path.isfile(theme_headers_file)):
        tmp = configurator.get_yaml(theme_headers_file)
        # theme headers file might only define entries for pages
        if (tmp[buildingfor]):
            theme_headers = tmp

    # Parse remainder (header content)
    processed_entries = _process_header_dict(theme_headers[buildingfor], args.header_content)
    final_entries = _remove_temporary_entries(processed_entries)

    # Generate article file name from user / default template
    file_name = _get_article_path(args, user_config, processed_entries, page)

    logging.debug("Creating new article file at " + file_name)

    with open(file_name, 'w+') as stream:
        stream.write(_get_new_article(final_entries))

    logging.debug("Done creating article.")

def configure_logging(debugLevel):
    """ Configure logging according to passed debug level. """

    if(debugLevel == 1):
        logging.basicConfig(level=logging.INFO)
    elif(debugLevel >= 2):
        logging.basicConfig(level=logging.DEBUG)
