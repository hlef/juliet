import argparse, yaml, logging, os, slugify, datetime, sys
from juliet import configurator, loader, paths, defaults, version
from juliet.builder import Builder
from string import Template

def main():
    """ Parse command line arguments and execute passed subcommands. """

    args = parse_arguments(sys.argv[1:])
    configure_logging(args.debug)

    if(args.subcommand == "build"):
        logging.debug("Executing sub-command " + args.subcommand)
        build(args)
    elif(args.subcommand == "init"):
        logging.debug("Executing sub-command " + args.subcommand)
        init(args)
    elif(args.subcommand == "new"):
        logging.debug("Executing sub-command " + args.subcommand)
        init_new_article(args)

    logging.debug("Done. Exiting.")

def build(args):
    """ Build website to configured location. """

    logging.info("Parsing configuration...")
    try:
        config = {"site": configurator.get_config(os.path.join(args.src, args.configfile))}
    except:
        sys.exit("Error during configuration, " + str(exc))

    logging.info("Loading and pre-processing content...")
    if (os.path.isdir(os.path.join(args.src, paths.POSTS_PATH))):
        config["posts"] = loader.get_from_folder(os.path.join(args.src, paths.POSTS_PATH), config)
    else:
        config["posts"] = {}

    if (os.path.isdir(os.path.join(args.src, paths.PAGES_PATH))):
        config["pages"] = loader.get_from_folder(os.path.join(args.src, paths.PAGES_PATH), config)
    else:
        config["pages"] = {}

    logging.debug("Configuring Jinja2 environment...")
    jinjaEnv = configurator.configure_jinja(config["site"]["theme"], args.src)

    logging.debug("Initializing builder...")
    builder = Builder(jinjaEnv, config, args.src, args.dest, args.noclean)
    builder.build()

def init(args):
    """ Initialize a new, clean website in passed directory."""

    logging.debug("Creating source directories")
    for directory in paths.SOURCE_DIRS:
        os.makedirs(os.path.join(args.dir, directory), exist_ok=True)

    logging.debug("Importing default config.yml")
    with open(os.path.join(args.dir, paths.CFG_FILE), 'w+') as stream:
        stream.write(defaults.default_config)

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

    parser_init = subparsers.add_parser('init', parents=[parent_parser],
    help="Initialize a new, clean website in current directory.")

    parser_init.add_argument('--dir', dest="dir", type=str,
                    default=paths.DEFAULT_INITDIR,
                    help='Initialize website in passed directory')

    parser_new = subparsers.add_parser('new', parents=[parent_parser],
    help="Initialize a fresh, new article file.")

    parser_new.add_argument('--build-src', '-s', dest="src", type=str, default="",
                    help='juliet source directory where to initialize article')

    parser_new.add_argument('--file-name', '-f', dest="file_name", nargs='?',
                            default=None, help='file name for new article')

    parser_new.add_argument('header_content', default=[],
    nargs=argparse.REMAINDER, help='header content of the new article')

    return main_parser.parse_args(args)

def _parse_raw_header_entries(header_entries):
    """ TODO """

    def __check_key(key):
        if ("_" in key or " " in key or ":" in key or not len(key)):
            return False
        return True

    result = {}
    if (len(header_entries) < 1):
        return result

    # Remove leading '--'
    header_entries = header_entries[1:]
    if (not len(header_entries) % 2 == 0):
        raise ValueError("last key does not have a value")

    while (len(header_entries)):
        # Retrieve raw key
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

def _get_article_path(args, user_config, processed_entries):
    """ Return article path matching passed args. """

    article_filename = ""
    if (args.file_name):
        article_filename = args.file_name
    elif ("filenaming_pattern" in user_config.keys()):
        article_filename = Template(user_config["filenaming_pattern"]).substitute(**processed_entries)
    else:
        article_filename = Template(defaults.DEFAULT_FILE_NAMING_PATTERN).substitute(**processed_entries)

    return os.path.join(args.src, paths.POSTS_BUILDDIR, article_filename)

def _process_header_dict(theme_config, parsed_entries):
    """ TODO """

    # Add parsed entries
    merged = parsed_entries.copy()

    # Fix missing entries with theme's defaults
    for key, value in theme_config.items():
        if (value[0] not in merged.keys() and value[1]):
            merged[key] = value[1]

    # Apply modifiers
    result = merged.copy()
    for key, value in merged.items():
        result["slug_" + key] = slugify.slugify(value)
        if (key == "date"):
            result["date_"] = merged[key]

    # Generate date_ if not already in result
    if ("date_" not in result.keys()):
        result["date_"] = datetime.date.today().strftime("%Y-%m-%d")

    return result

def init_new_article(args):
    """ Initialize a fresh, new article file. """

    def _apply_theme_configuration(theme_config, processed_entries):
        result = {}
        for key, value in theme_config.items():
            result[key] = processed_entries[value[0]]

        return result

    def _get_new_article(final_header):
        default_article = "---\n" + yaml.dump(final_header, default_flow_style=False) + "---"
        return default_article

    # Get configs
    user_config = configurator.get_config(os.path.join(args.src, paths.CFG_FILE))
    if (not user_config):
        logging.error("Error, could not find user config at {}".format(os.path.join(args.src, paths.CFG_FILE)))
        return

    theme_config = {}
    theme_cfg_file = os.path.join(args.src, paths.THEMES_PATH, user_config["theme"], paths.CFG_FILE)
    if (os.path.isfile(theme_cfg_file)):
        theme_config = configurator.get_config(theme_cfg_file)
    else:
        theme_config = defaults.DEFAULT_THEME_CFG

    # Parse remainder (header content)
    parsed_entries = _parse_raw_header_entries(args.header_content)
    processed_entries = _process_header_dict(theme_config, parsed_entries)
    final_entries = _apply_theme_configuration(theme_config, processed_entries)

    # Generate article file name from user / default template
    file_name = _get_article_path(args, user_config, processed_entries)

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
