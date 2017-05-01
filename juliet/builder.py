#!/usr/bin/python3

import os, logging
from distutils.dir_util import copy_tree
from jinja2 import Template, FileSystemLoader
from juliet import paths

def _createIfNonExistent(directory):
    """ Create passed directory if it doesn't exists already. """

    if not os.path.exists(directory):
        logging.debug("Creating directory " + directory)
        os.makedirs(directory)
    else:
        logging.warning("Writing to existing directory " + directory)

def _write(directory, string):
    """ Write passed string to passed directory. """

    with open(directory, 'w') as stream:
        stream.write(string)

def _formatArgsAndRender(args, page, template):
    """ Add required entries to rendering args and return rendered template. """

    renderingArgs = args
    renderingArgs["page"] = page
    renderingArgs["content"] = page["body"]
    return template.render(args)

def installData(args):
    """ Install data and assets. """

    builddir = args["site"]["build-directory"]
    _createIfNonExistent(builddir)

    copy_tree(paths.THEMES_PATH + "/" + args["site"]["theme"] + "/data/",
              builddir + "/" + paths.DATA_BUILDDIR)
    copy_tree(paths.ASSETS_PATH, builddir + "/" + paths.ASSETS_BUILDDIR)

def buildStatics(args, jinjaEnv):
    """ Build static pages. """

    builddir = args["site"]["build-directory"]
    _createIfNonExistent(builddir)

    for element in os.listdir(paths.THEMES_PATH + "/" + args["site"]["theme"] + "/statics/"):
        html = jinjaEnv.get_template("statics/" + element).render(args)
        _write(builddir + "/" + element, html)

def buildPosts(args, jinjaEnv):
    """ Build posts. """

    builddir = args["site"]["build-directory"] + "/" + paths.POSTS_BUILDDIR
    _createIfNonExistent(builddir)

    template = jinjaEnv.get_template("templates/posts.html")

    for post in args["posts"]:
        html = _formatArgsAndRender(args, post, template)
        _write(builddir + "/" + post["slug"], html)

def buildPages(args, jinjaEnv):
    """ Build pages. """

    builddir = args["site"]["build-directory"]
    _createIfNonExistent(builddir)

    template = jinjaEnv.get_template("templates/pages.html")

    for page in args["pages"]:
        html = _formatArgsAndRender(args, page, template)
        _write(builddir + "/" + page["permalink"], html)
