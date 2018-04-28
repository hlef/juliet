__version__ = '0.1-final'
__author__ = 'Hugo Lefeuvre'
__author_email__ = 'hle@owl.eu.com'

import argparse, logging, os, slugify, datetime
from juliet import configurator, loader, paths, defaults
from juliet.builder import Builder

def main():
    """ Parse command line arguments and execute passed subcommands. """

    args = parse_arguments()
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
    config = {"site": configurator.get_config(os.path.join(args.src, paths.CFG_FILE))}

    logging.info("Loading and pre-processing content...")
    config["posts"] = loader.get_from_folder(os.path.join(args.src, paths.POSTS_PATH), config)
    config["pages"] = loader.get_from_folder(os.path.join(args.src, paths.PAGES_PATH), config)

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
    with open(os.path.join(args.dir, paths.CFG_FILE), 'w') as stream:
        stream.write(defaults.default_config)

def init_new_article(args):
    """ Initialize a fresh, new article file. """

    file_name = os.path.join(args.src, paths.POSTS_BUILDDIR, args.date + '-' + slugify.slugify(args.title))

    logging.debug("Creating new article file...")

    with open(file_name, 'w') as stream:
        # TODO: Support importing header generator from juliet template
        stream.write(defaults.default_article.format(args.title, args.date))

    logging.debug("Done creating article.")

def parse_arguments():
    """ Parse and return arguments. """

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--debug', '-d', action='count', default=0)
    parent_parser.add_argument('--version', action='version',
                       version='%(prog)s {version}'.format(version=__version__))

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

    parser_init = subparsers.add_parser('init', parents=[parent_parser],
    help="Initialize a new, clean website in current directory.")

    parser_init.add_argument('--dir', dest="dir", type=str,
                    default=paths.DEFAULT_INITDIR,
                    help='Initialize website in passed directory')

    parser_new = subparsers.add_parser('new', parents=[parent_parser],
    help="Initialize a fresh, new article file.")

    parser_new.add_argument('--build-src', '-s', dest="src", type=str, default="",
                    help='juliet source directory where to initialize article')

    parser_new.add_argument('--date', dest="date", type=_valid_date_argparse,
                    default=datetime.date.today().strftime("%Y-%m-%d"),
                    help='date of the article - format YYYY-MM-DD')

    parser_new.add_argument('--title', '-t', dest="title", type=str, required=True,
                    help='title of the article')

    return main_parser.parse_args()

def _valid_date_argparse(s):
    try:
        datetime.datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        msg = "Passed date is incorrectly formatted: '{0}' (YYYY-MM-DD expected).".format(s)
        raise argparse.ArgumentTypeError(msg)

def configure_logging(debugLevel):
    """ Configure logging according to passed debug level. """

    if(debugLevel == 1):
        logging.basicConfig(level=logging.INFO)
    elif(debugLevel >= 2):
        logging.basicConfig(level=logging.DEBUG)
