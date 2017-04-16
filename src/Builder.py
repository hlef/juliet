#!/usr/bin/python3

import os
from jinja2 import Template
from src import FileParser

def buildStatics(args):
    """ Build static pages. """

    builddir = args["site"]["build-directory"]

    if not os.path.exists(builddir):
        os.makedirs(builddir)

    for static in args["statics"]:
        # Render static page
        # TODO static pages should also allow layouts !
        html = Template(static["body"]).render(args)

        # Save static pgae
        with open(builddir + "/" + static["file-name"], 'w') as stream:
            stream.write(html)

def buildPosts(args, jinjaEnv):
    """ Build posts. """

    postBuilddir = args["site"]["build-directory"] + "/posts/"

    if not os.path.exists(postBuilddir):
        os.makedirs(postBuilddir)

    # Pre-render post template.
    template = jinjaEnv.get_template("templates/posts.html")

    for post in args["posts"]:
        # Render post
        renderingArgs = args
        renderingArgs["page"] = post
        renderingArgs["content"] = post["body"]
        html = template.render(args)

        # Save post
        with open(postBuilddir + post["title-slugified"], 'w') as stream:
            stream.write(html)

def buildPages(args, jinjaEnv):
    """ Build pages. """

    builddir = args["site"]["build-directory"]

    if not os.path.exists(builddir):
        os.makedirs(builddir)

    # Pre-render post template.
    template = jinjaEnv.get_template("templates/pages.html")

    for page in args["pages"]:
        # Render page
        renderingArgs = args
        renderingArgs["page"] = page
        renderingArgs["content"] = page["body"]
        html = template.render(args)

        # Save page
        with open(builddir + page["permalink"], 'w') as stream:
            stream.write(html)
