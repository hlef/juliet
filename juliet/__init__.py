import argparse
from juliet import configurator, builder, loader, paths

def main():
    """ Parse command line arguments and execute passed subcommands. """

    # Parse subcommand
    parser = argparse.ArgumentParser(description='The lightweight static website generator')
    subparsers = parser.add_subparsers(dest="sp", help="sub-command to be executed")

    parser_build = subparsers.add_parser('build',
    help="Build static site from local directory to the directory specified in config.yml")

    parser_build.add_argument('--config', type=str, default=paths.CFG_FILE,
                    help='alternative config file to use instead of config.yml')

    args = parser.parse_args()

    # Execute passed sub-command or return error
    if(args.sp == "build"):
        build(args)

def build(args):
    """ Build website to configured location. """

    # Parse configuration
    config = {"site": configurator.getConfig(args.config)}

    # Load articles and pages from the files
    config["posts"] = loader.getFromFolder(paths.POSTS_PATH, config)
    config["pages"] = loader.getFromFolder(paths.PAGES_PATH, config)

    # Configure Jinja2 environment
    jinjaEnv = configurator.configureJinja(config["site"])

    # Build statics
    builder.buildStatics(config, jinjaEnv)

    # Build posts and pages
    builder.buildPosts(config, jinjaEnv)
    builder.buildPages(config, jinjaEnv)

    # Install remaining data
    builder.installData(config)
