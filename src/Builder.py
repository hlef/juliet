#!/usr/bin/python3

import os
from jinja2 import Template
from src import FileParser

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

def buildStatics(args):
    """ Build static pages. """

    builddir = args["site"]["build-directory"]
    _createIfNonExistent(builddir)

    for static in args["statics"]:
        html = Template(static["body"]).render(args)
        _write(builddir + "/" + static["file-name"], html)

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
        _write(builddir + page["permalink"], html)
