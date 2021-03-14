import os, logging, shutil
from distutils.dir_util import copy_tree
from jinja2 import Template, FileSystemLoader
from juliet import paths

class Builder:
    def __init__(self, jinja_env, build_args, src, dest, noclean):
        """ Constructor for class Builder. Takes a jinja Environment and the
        build arguments dictionnary as argument. """

        self.jinja_env = jinja_env
        self.build_args = build_args
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

        if(not self._is_safe_path(path)):
            raise ValueError("Trying to build element to unsafe path (" +
                             path + " outside of " + self.destination + ").")

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path)) # may raise OSError

        with open(path, 'w') as stream:
            stream.write(string)

    def _format_args_and_render(self, page, template):
        """ Render passed template as a page/post template and return it. """

        rendering_args = self.build_args
        rendering_args["page"] = page
        rendering_args["content"] = page["body"]
        return template.render(rendering_args)

    def _install_data(self):
        """ Install data and assets. """

        data_path = os.path.join(self.source, paths.THEMES_PATH, self.build_args["site"]["theme"], "data")
        assets_path = os.path.join(self.source, paths.ASSETS_PATH)

        if (os.path.exists(data_path)):
            copy_tree(data_path, os.path.join(self.destination, paths.DATA_BUILDDIR))
        if (os.path.exists(assets_path)):
            copy_tree(assets_path, os.path.join(self.destination, paths.ASSETS_BUILDDIR))

    def _build_statics(self):
        """ Build static pages and install them. """

        statics_path = os.path.join(self.source, paths.THEMES_PATH, self.build_args["site"]["theme"], "statics")

        # statics folder might very well not exist if theme doesn't define one
        if (os.path.exists(statics_path)):
            for element in os.listdir(statics_path):
                html = self.jinja_env.get_template(os.path.join("statics", element)).render(self.build_args)
                self._write(os.path.join(self.destination, element), html)

    def _build_posts(self):
        """ Build posts and install them. """

        self._build_entry_common("posts", paths.POSTS_BUILDDIR)

    def _build_pages(self):
        """ Build pages and install them. """

        self._build_entry_common("pages", paths.PAGES_BUILDDIR)

    def _build_entry_common(self, entrytype, builddir):
        if (not len(self.build_args[entrytype])):
            return

        builddir = os.path.join(self.destination, builddir)
        os.makedirs(builddir, exist_ok=True)

        template = self.jinja_env.get_template(os.path.join("templates", entrytype + ".html"))

        for entry in self.build_args[entrytype]:
            html = self._format_args_and_render(entry, template)
            os.makedirs(os.path.dirname(os.path.abspath(entry["installed_filename"])), exist_ok=True)
            self._write(os.path.join(builddir, entry["installed_filename"]), html)

    def _is_safe_path(self, path, follow_symlinks=False):
        """ Check directories before writing to avoid directory traversal. """

        if follow_symlinks:
            return os.path.realpath(path).startswith(os.path.realpath(self.destination))
        return os.path.abspath(path).startswith(os.path.abspath(self.destination))
