#!/usr/bin/python3

import os, logging
from distutils.dir_util import copy_tree
from jinja2 import Template, FileSystemLoader
from juliet import paths

class Builder:
    def __init__(self, jinjaEnv, buildArgs):
        """ Constructor for class Builder. Takes a jinja Environment and the
        build arguments dictionnary as argument. """

        self.jinjaEnv = jinjaEnv
        self.buildArgs = buildArgs

    def _createIfNonExistent(self, directory):
        """ Create passed directory if it doesn't exist already. """

        if not os.path.exists(directory):
            logging.debug("Creating directory " + directory)
            os.makedirs(directory)
        else:
            logging.warning("Writing to existing directory " + directory)

    def _write(self, path, string):
        """ Write passed string to passed path. """

        with open(path, 'w') as stream:
            stream.write(string)

    def _formatArgsAndRender(self, page, template):
        """ Add required entries to rendering args and return rendered template. """

        renderingArgs = self.buildArgs
        renderingArgs["page"] = page
        renderingArgs["content"] = page["body"]
        return template.render(renderingArgs)

    def installData(self):
        """ Install data and assets. """

        builddir = self.buildArgs["site"]["build-directory"]
        datadir = paths.THEMES_PATH + "/" + self.buildArgs["site"]["theme"] + "/data/"

        self._createIfNonExistent(builddir)

        copy_tree(datadir, builddir + "/" + paths.DATA_BUILDDIR)
        copy_tree(paths.ASSETS_PATH, builddir + "/" + paths.ASSETS_BUILDDIR)

    def buildStatics(self):
        """ Build static pages. """

        builddir = self.buildArgs["site"]["build-directory"]
        staticsdir = paths.THEMES_PATH + "/" + self.buildArgs["site"]["theme"] + "/statics/"
        self._createIfNonExistent(builddir)

        for element in os.listdir(staticsdir):
            html = self.jinjaEnv.get_template("statics/" + element).render(self.buildArgs)
            self._write(builddir + "/" + element, html)

    def buildPosts(self):
        """ Build posts. """

        builddir = self.buildArgs["site"]["build-directory"] + "/" + paths.POSTS_BUILDDIR
        self._createIfNonExistent(builddir)

        template = self.jinjaEnv.get_template("templates/posts.html")

        for post in self.buildArgs["posts"]:
            html = self._formatArgsAndRender(post, template)
            self._write(builddir + "/" + post["slug"], html)

    def buildPages(self):
        """ Build pages. """

        builddir = self.buildArgs["site"]["build-directory"]
        self._createIfNonExistent(builddir)

        template = self.jinjaEnv.get_template("templates/pages.html")

        for page in self.buildArgs["pages"]:
            html = self._formatArgsAndRender(page, template)
            self._write(builddir + "/" + page["permalink"], html)
