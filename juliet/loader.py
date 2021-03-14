import os, sys, logging, juliet
from juliet.pageprocessor import PageProcessor

def _load_from_file(processor, folder, path):
    logging.debug("Loading file " + path)

    element = {}
    with open(os.path.join(folder, path), 'r') as stream:
        element = processor.process(stream.read(), path)

    return element

def get_from_folder(folder, config):
    """ Load files contained in passed folder, pre-process them using fileParser
    and return them as a list sorted in inverse alphabetical order.

    Files in passed folder should have a valid Page format (see FileParser). """

    elements = []
    entries = sorted(os.listdir(folder), reverse=True)

    file_naming_var = ""
    if ("file_naming_variable" in config["site"].keys()):
        file_naming_var = config["site"]["file_naming_variable"]
    else:
        file_naming_var = juliet.defaults.DEFAULT_FILE_NAMING_VARIABLE

    theme_headers = juliet.defaults.DEFAULT_THEME_HEADERS
    theme_headers_file = os.path.join(config["site"]["baseurl"], juliet.paths.THEMES_PATH,
        config["site"]["theme"], juliet.paths.THEME_HEADERS_FILE)
    if (os.path.isfile(theme_headers_file)):
        tmp = juliet.configurator.get_yaml(theme_headers_file)
        # theme headers file might only define entries for posts/pages
        if (tmp[folder]):
            theme_headers = tmp

    processor = PageProcessor(config["site"]["baseurl"], file_naming_var)
    for source_file in entries:
        elements.append(_load_from_file(processor, folder, source_file))

        for key, value in theme_headers.items():
            if (key not in elements[-1].keys() and value):
                # Fix missing entries with theme's defaults
                elements[-1][key] = value

    return elements
