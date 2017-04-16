#!/usr/bin/python3

import argparse, sys

from src import Configurator, Builder, Loader

def main():
    """ Parse command line arguments and execute passed subcommands. """

    # Parse subcommand
    parser = argparse.ArgumentParser(description='Pythonic static sites generator')
    subparsers = parser.add_subparsers(dest="sp", help="sub-command to be executed")

    parser_build = subparsers.add_parser('build', help="Build static site from local directory")

    args = parser.parse_args()

    # Execute passed sub-command or return error
    if(args.sp == "build"):
        build(args)

def build(args):
    """ Build website to configured location. """

    # Parse configuration
    config = {}
    config["site"] = Configurator.getConfig()

    # Load articles and pages from the files
    config["posts"] = Loader.getFromFolder("posts/", args)
    config["pages"] = Loader.getFromFolder("pages/", args)

    # Configure Jinja2 environment
    jinjaEnv = Configurator.configureJinja(config["site"])
    print(config)

    # Build statics
    Builder.buildStatics(config, jinjaEnv)

    # Build posts and pages
    Builder.buildPosts(config, jinjaEnv)
    Builder.buildPages(config, jinjaEnv)

    # Install remaining data
    Builder.installData(config)

if __name__ == "__main__":
    main()
