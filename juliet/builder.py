#!/usr/bin/python3

import os, logging
from distutils.dir_util import copy_tree
from jinja2 import Template, FileSystemLoader
from juliet import paths

class Builder:
    def __init__(self, jinjaEnv, buildArgs, src, dest):
        """ Constructor for class Builder. Takes a jinja Environment and the
        build arguments dictionnary as argument. """

        self.jinjaEnv = jinjaEnv
        self.buildArgs = buildArgs
        self.source = src
        self.destination = dest

    def build(self):
        """ Build and install the website as described in the configuration. """

        self._createIfNonExistent(self.destination)

        logging.info("Building static pages...")
        self._buildStatics()

        logging.info("Building posts and pages...")
        self._buildPosts()
        self._buildPages()

        logging.info("Installing assets...")
        self._installData()

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
        """ Render passed template as a page/post template and return it. """

        renderingArgs = self.buildArgs
        renderingArgs["page"] = page
        renderingArgs["content"] = page["body"]
        return template.render(renderingArgs)

    def _installData(self):
        """ Install data and assets. """

        assets_path = os.path.join(self.source, paths.ASSETS_PATH)
        data_path = os.path.join(self.source, paths.THEMES_PATH, self.buildArgs["site"]["theme"], "data")

        copy_tree(data_path, os.path.join(self.destination, paths.DATA_BUILDDIR))
        copy_tree(assets_path, os.path.join(self.destination, paths.ASSETS_BUILDDIR))

    def _buildStatics(self):
        """ Build static pages and install them. """

        staticsdir = os.path.join(self.source, paths.THEMES_PATH, self.buildArgs["site"]["theme"], "statics")

        for element in os.listdir(staticsdir):
            html = self.jinjaEnv.get_template(os.path.join("statics", element)).render(self.buildArgs)
            self._write(os.path.join(self.destination, element), html)

    def _buildPosts(self):
        """ Build posts and install them. """

        builddir = os.path.join(self.destination, paths.POSTS_BUILDDIR)
        self._createIfNonExistent(builddir)

        template = self.jinjaEnv.get_template(os.path.join("templates", "posts.html"))

        for post in self.buildArgs["posts"]:
            html = self._formatArgsAndRender(post, template)
            self._write(os.path.join(builddir, post["slug"]), html)

    def _buildPages(self):
        """ Build pages and install them. """

        template = self.jinjaEnv.get_template(os.path.join("templates", "pages.html"))

        for page in self.buildArgs["pages"]:
            html = self._formatArgsAndRender(page, template)
            self._write(os.path.join(self.destination, page["permalink"]), html)
