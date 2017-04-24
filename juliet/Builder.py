#!/usr/bin/python3

import os
from distutils.dir_util import copy_tree
from jinja2 import Template, FileSystemLoader
from juliet import FileParser

def _createIfNonExistent(directory):
    """ Create passed directory if it doesn't exists already. """

    if not os.path.exists(directory):
        os.makedirs(directory)

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

    copy_tree("themes/" + args["site"]["theme"] + "/data/", builddir)
    copy_tree("assets/", builddir + "/assets")

def buildStatics(args, jinjaEnv):
    """ Build static pages. """

    builddir = args["site"]["build-directory"]
    _createIfNonExistent(builddir)

    for element in os.listdir("themes/" + args["site"]["theme"] + "/statics/"):
        html = jinjaEnv.get_template("statics/" + element).render(args)
        _write(builddir + "/" + element, html)

def buildPosts(args, jinjaEnv):
    """ Build posts. """

    builddir = args["site"]["build-directory"] + "/posts/"
    _createIfNonExistent(builddir)

    template = jinjaEnv.get_template("templates/posts.html")

    for post in args["posts"]:
        html = _formatArgsAndRender(args, post, template)
        _write(builddir + post["slug"], html)

def buildPages(args, jinjaEnv):
    """ Build pages. """

    builddir = args["site"]["build-directory"]
    _createIfNonExistent(builddir)

    template = jinjaEnv.get_template("templates/pages.html")

    for page in args["pages"]:
        html = _formatArgsAndRender(args, page, template)
        _write(builddir + "/" + page["permalink"], html)
