DEFAULT_THEME_NAME = "gram"

# "config.yml required entry": can be empty
CONFIG_REQUIRED_ENTRIES = {"baseurl": True, "theme": False}

DEFAULT_FILE_NAMING_VARIABLE = "title"
DEFAULT_FILE_NAMING_PATTERN = "$date_-$slug_title.md"
DEFAULT_PAGE_NAMING_PATTERN = "$slug_title.md"
DEFAULT_THEME_HEADERS = {
    "posts": {
        "title": "Default post title",
        "date": None
    },
    "pages": {
        "title": "Default page title",
    }
}
