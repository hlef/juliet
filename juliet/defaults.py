DEFAULT_THEME_NAME = "bare"
DEFAULT_CONFIG = (
"""# useful when your website isn't located at the root of your server
baseurl: ""

# the directory in themes/ that contain your theme
# WARNING: No theme under themes/ yet ! More informations in the documentation:
# https://github.com/hlef/juliet
theme: "{}"
""").format(DEFAULT_THEME_NAME)

# "config.yml required entry": can be empty
CONFIG_REQUIRED_ENTRIES = {"baseurl": True, "theme": False}

DEFAULT_FILE_NAMING_VARIABLE = "title"
DEFAULT_FILE_NAMING_PATTERN = "$date_-$slug_title.md"
DEFAULT_THEME_CFG = {"title": ["title", "Default title"],
                     "date": ["date_", None]}
