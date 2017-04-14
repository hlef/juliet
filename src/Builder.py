#!/usr/bin/python3

import os
from jinja2 import Template

def buildStatics(args):
    """ Build static pages. """

    themesdir = "themes/{}/statics/".format(args["site"]["theme"])
    builddir = args["site"]["build-directory"]

    for templateFile in os.listdir(themesdir):
        # Render page
        html = ""
        with open(themesdir + templateFile, 'r') as stream:
            page = stream.read()
            html = Template(page).render(args)

        # Save page
        with open(builddir + templateFile, 'w') as stream:
            stream.write(html)

def buildPosts(args, jinjaEnv):
    """ Build templated pages. """

    builddir = args["site"]["build-directory"]

    for post in args["posts"]:
        # Render page
        renderingArgs = args
        renderingArgs["post"] = post
        html = jinjaEnv.get_template('post.html').render(args)

        # Save page
        with open(builddir + "/posts/" + post["title-slugified"], 'w') as stream:
            stream.write(html)
