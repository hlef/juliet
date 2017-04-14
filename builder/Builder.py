#!/usr/bin/python3

import jinja2

def getStatics():
    pass

def getPosts():
    pass

def build(template, params):
    """ Build HTML documents from passed jinja files and parameters. """
    pass

def buildStatics(config):
    """ Build static pages. """

    statics = getStatics()
    for staticPage in statics:
        build(staticPage, config)

def buildPosts(config, jinjaEnv):
    """ Build templated pages. """

    posts = getPosts()
    for post in posts:
        build(jinjaEnv.get_template("post.html"), post+config)
