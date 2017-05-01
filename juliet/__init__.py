import argparse, logging
from juliet import configurator, builder, loader, paths

def main():
    """ Parse command line arguments and execute passed subcommands. """

    # PARENT PARSER (for debug, etc.)
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--debug', '-d', action='count', default=0)

    # MAIN PARSER
    main_parser = argparse.ArgumentParser(description='The lightweight static website generator',
                    parents=[parent_parser])

    # BUILD SUBPARSER
    subparsers = main_parser.add_subparsers(dest="subcommand", help="sub-command to be executed")
    subparsers.required = True

    parser_build = subparsers.add_parser('build', parents=[parent_parser],
    help="Build static site from local directory to the directory specified in config.yml")

    parser_build.add_argument('--config', type=str, default=paths.CFG_FILE,
                    help='alternative config file to use instead of config.yml')

    # Parse arguments
    args = main_parser.parse_args()

    # Configure logging
    if(args.debug == 1):
        logging.basicConfig(level=logging.INFO)
    elif(args.debug >= 2):
        logging.basicConfig(level=logging.DEBUG)

    # Execute passed sub-command or return error
    if(args.subcommand == "build"):
        logging.debug("Executing sub-command build")
        build(args)

    logging.debug("Done. Exiting.")

def build(args):
    """ Build website to configured location. """

    logging.info("Parsing configuration...")
    config = {"site": configurator.getConfig(args.config)}

    logging.info("Loading and parsing content...")
    config["posts"] = loader.getFromFolder(paths.POSTS_PATH, config)
    config["pages"] = loader.getFromFolder(paths.PAGES_PATH, config)

    logging.debug("Configuring Jinja2 environment...")
    jinjaEnv = configurator.configureJinja(config["site"])

    logging.info("Building static pages...")
    builder.buildStatics(config, jinjaEnv)

    logging.info("Building posts and pages...")
    builder.buildPosts(config, jinjaEnv)
    builder.buildPages(config, jinjaEnv)

    logging.info("Installing assets...")
    builder.installData(config)
