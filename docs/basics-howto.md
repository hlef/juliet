# Juliet *- basics*

## File structure

Juliet website sources are organized as following:

    .
    ├── assets
    │   └── ...
    ├── config.yml
    ├── pages
    │   └── ...
    ├── posts
    │   └── ...
    └── themes
        └── yourtheme
            └── ...

`juliet init` can initialize this file structure for you in the current directory.

The default theme is [gram](https://github.com/hlef/juliet-gram-theme).

We recommend you to either pick and install one of our recommended themes (see
`docs/recommended-themes.md`), or be creative and design your own one! You will
find more information about theme design in `docs/themes-howto.md`.

### :wrench: Build configuration, *config.yml*

`config.yml` is the configuration file of your website. It defines *variables*
needed by the build system, by your theme, and static pages.

Following variables are required by the build system and are thus mandatory for
any Juliet config file:

    # useful when your website isn't located at the root of your server
    baseurl: ""

    # the directory in themes/ that contain your theme
    theme: sample_theme

The set of required entries in the configuration file may vary depending on your
theme. You can usually find more informations about it in your theme directory,
under `themes/your_theme/README`.

### :pencil: Blog posts, *posts/*

Juliet posts go to the `posts/` directory and are divided in two parts:
 * The *header*, containing YAML-formatted informations about the post
 * The post's *body*, in in the original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax) with
 preprocessor tags (see dedicated paragraph)

For example:

    ---
    title: "Hello, world!"
    date: 2016-04-06 16:07:35
    ---

    Hello, **world**!

Juliet defines some special entries which will alter the behavior of the engine:
 * `permalink` allows you to specify *where exactly* to install the article.
   Works for both posts and pages.

Apart from these, the set of required entries in post headers varies depending
on your theme. You can find more informations about it in your theme directory,
under `themes/your_theme/README`.

Please, note that even if it is empty, the header has to be present.

#### Creating a fresh article file

Because creating a fresh article structure each and every time you write a new
article is repetitive and annoying, Juliet >= 0.2 adds support for the
`juliet new` feature which takes care of it for you.

Pro tip: you can get more information about this feature via `juliet new --help`.

### :bookmark: Preprocessor tags
#### Pygments syntax highlighting

Juliet provides native integration of [Pygments](http://pygments.org/) syntax
highlighting, via the [python-markdown library](https://python-markdown.github.io/extensions/code_hilite/).

#### Base url inclusion

If you want to refer to the baseurl variable specified in the config file,
simply use the Jinja-like `{{ baseurl }}` tag.

Escaping with backslash is supported. For example if you want to write
`{{ baseurl }}` without having it replaced by the preprocessor, you'll
simply have to write `\{{ baseurl }}`.

### :house: Site pages, *pages/*

Pages go to the `pages/` directory and follow the same header/body structure as
posts with the same rules.

Required header entries might be different to the ones required for posts. You
can find more informations about it in the README file of your theme.

### :metal: Themes

Juliet themes are organized as following:

    .
    ├── data
    │   ├── css
    │   │   └── ...
    │   └── js
    │       └── ...
    ├── includes
    │   └── ... (ex: head.html, navbar.html, etc.)
    ├── README
    ├── LICENSE (optional)
    ├── config.yml.EX (optional)
    ├── statics
    │   ├── index.html
    │   └── ...
    └── templates
        ├── pages.html
        ├── posts.html
        └── ...

Most important things:

 * files placed under data/ will be copied as-is to the root directory of your website.
 * files placed at the root of the theme directory are ignored by the build system.
   `README`, `LICENSE`, `config.yml.EX` are only present for the sake of documentation.

You can find more informations about theming in `docs/themes-howto.md`.

## Building the beast

Build the website using the `juliet build` command. It will build the website
in `build-area` by default. Alternatively, you may want to specify a destination
using `--build-dst`.

You can also specify the source directory via `--build-src`.

### :file_folder: Installed structure

    .
    ├── page1.html
    ├── page2.html
    ├── ...
    ├── index.html
    ├── static2.html
    ├── ...
    ├── assets
    │   ├── ...
    ├── css
    │   ├── ...
    ├── favicon
    │   ├── ...
    ├── fonts
    │   ├── ...
    ├── index.html
    ├── js
    │   └── ...
    └── posts
        ├── ...

Unless `permalink` is defined in page/post headers, pages are installed at the
root of the build area, and posts under `posts/`.

Also, unless `permalink` is defined the name under which pages/posts will be
installed is defined by the file naming variable. By default the file naming
variable is defined as the "title" entry, but this can be changed by defining
the `file_naming_variable` field in `config.yml`.
