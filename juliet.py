#!/usr/bin/python3

import argparse, sys

from config import Configurator
from builder import Builder

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

    # Parse configuration and define Environment
    config = Configurator.getConfig()
    Builder.setConfig(config)

    # Build statics
    Builder.buildStatics()

    # Build posts and pages
    Builder.buildTemplated()

if __name__ == "__main__":
    main()
