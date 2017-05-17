import argparse, logging, os
from juliet import configurator, loader, paths
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
    builder = Builder(jinjaEnv, config, args.src, args.dest)
    builder.build()

def init(args):
    """ Initialize a new, clean website in passed directory."""

    raise NotImplementedError("Not implemented yet")

def parse_arguments():
    """ Parse and return arguments. """

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--debug', '-d', action='count', default=0)

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

    parser_init = subparsers.add_parser('init', parents=[parent_parser],
    help="Initialize a new, clean website in current directory.")

    parser_init.add_argument('--dir', dest="dir", type=str,
                    default=paths.DEFAULT_INITDIR,
                    help='Initialize website in passed directory')

    return main_parser.parse_args()

def configure_logging(debugLevel):
    """ Configure logging according to passed debug level. """

    if(debugLevel == 1):
        logging.basicConfig(level=logging.INFO)
    elif(debugLevel >= 2):
        logging.basicConfig(level=logging.DEBUG)
