#!/usr/bin/python3

import os, logging, shutil
from distutils.dir_util import copy_tree
from jinja2 import Template, FileSystemLoader
from juliet import paths

class Builder:
    def __init__(self, jinjaEnv, buildArgs, src, dest, noclean):
        """ Constructor for class Builder. Takes a jinja Environment and the
        build arguments dictionnary as argument. """

        self.jinjaEnv = jinjaEnv
        self.buildArgs = buildArgs
        self.source = src
        self.destination = dest
        self.noclean = noclean

    def build(self):
        """ Build and install the website as described in the configuration. """

        if(not self.noclean):
            logging.info("Cleaning build folder " + self.destination)
            shutil.rmtree(self.destination, ignore_errors=True)

        os.makedirs(self.destination, exist_ok=True)

        logging.info("Building static pages...")
        self._build_statics()

        logging.info("Building posts and pages...")
        self._build_posts()
        self._build_pages()

        logging.info("Installing assets...")
        self._install_data()

    def _write(self, path, string):
        """ Write passed string to passed path. """

        with open(path, 'w') as stream:
            stream.write(string)

    def _format_args_and_render(self, page, template):
        """ Render passed template as a page/post template and return it. """

        renderingArgs = self.buildArgs
        renderingArgs["page"] = page
        renderingArgs["content"] = page["body"]
        return template.render(renderingArgs)

    def _install_data(self):
        """ Install data and assets. """

        assets_path = os.path.join(self.source, paths.ASSETS_PATH)
        data_path = os.path.join(self.source, paths.THEMES_PATH, self.buildArgs["site"]["theme"], "data")

        copy_tree(data_path, os.path.join(self.destination, paths.DATA_BUILDDIR))
        copy_tree(assets_path, os.path.join(self.destination, paths.ASSETS_BUILDDIR))

    def _build_statics(self):
        """ Build static pages and install them. """

        staticsdir = os.path.join(self.source, paths.THEMES_PATH, self.buildArgs["site"]["theme"], "statics")

        for element in os.listdir(staticsdir):
            html = self.jinjaEnv.get_template(os.path.join("statics", element)).render(self.buildArgs)
            self._write(os.path.join(self.destination, element), html)

    def _build_posts(self):
        """ Build posts and install them. """

        builddir = os.path.join(self.destination, paths.POSTS_BUILDDIR)
        os.makedirs(builddir, exist_ok=True)

        template = self.jinjaEnv.get_template(os.path.join("templates", "posts.html"))

        for post in self.buildArgs["posts"]:
            html = self._format_args_and_render(post, template)
            self._write(os.path.join(builddir, post["slug"]), html)

    def _build_pages(self):
        """ Build pages and install them. """

        template = self.jinjaEnv.get_template(os.path.join("templates", "pages.html"))

        for page in self.buildArgs["pages"]:
            html = self._format_args_and_render(page, template)
            self._write(os.path.join(self.destination, page["permalink"]), html)
