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

`juliet init` can initialize this file structure in the current directory.

The default theme is [gram](https://github.com/hlef/juliet-gram-theme).

Tip: You can either pick and install one of our recommended themes (see
`docs/recommended-themes.md`), or design your own one! You will find more
information about theme design in `docs/themes-howto.md`.

### :wrench: Build configuration, *config.yml*

Every juliet source has a `config.yml` file. It defines *variables* needed by
the build system, theme, and static pages.

Following variables are required by the build system and are thus mandatory for
any Juliet config file:

    # useful when your website isn't located at the root of your server
    baseurl: ""

    # the directory in themes/ that contain your theme
    theme: sample_theme

Required entries may vary depending on the theme. You can usually find more
informations about it in your theme directory, under
`themes/your_theme/README`!

### :pencil: Blog posts, *posts/*

Juliet posts are stored in `posts/`. Posts are organized in two parts:
 * The *header*, containing YAML-formatted informations about the post
 * The post's *body*, in in the original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax) with
   additions from [python-markdown](https://python-markdown.github.io/)

For example:

    ---
    title: "Hello, world!"
    date: 2016-04-06 16:07:35
    ---

    Hello, **world**!

Juliet defines some special entries which will alter the behavior of the engine:
 * `permalink` allows you to specify *where exactly* to install the article.
   Works for both posts and pages.

Required entries in post headers varies depending on your theme. You can find
more informations about it in your theme directory, under
`themes/your_theme/README`.

Please, note that even if it is empty, the header has to be present.

#### Creating a fresh article file

`juliet new` initializes a fresh article file.

For example:

    $ juliet new -- title "Karlsruhe, a beautiful city"
    $ cat posts/2019-08-08-karlsruhe-a-beautiful-city.md
    ---
    date: 2019-08-08
    title: Karlsruhe, a beautiful city
    ---

    $ juliet new -- title "Le Cuisinier françois" author "François Pierre La Varenne" date "21/12/1651"
    $ cat posts/1651-12-21-le-cuisinier-francois.md
    ---
    author: "François Pierre La Varenne"
    date: 1651-12-21
    title: "Le Cuisinier françois"
    ---

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

### Markdown extensions

#### Tables and footnotes

Tables and footnotes support is provided via python-markdown:
[tables](https://python-markdown.github.io/extensions/tables/),
[footnotes](https://python-markdown.github.io/extensions/footnotes/).

#### Pygments syntax highlighting

Juliet provides native integration of [Pygments](http://pygments.org/) syntax
highlighting, via the [python-markdown](https://python-markdown.github.io/extensions/code_hilite/).

#### Base url inclusion

If you want to refer to the baseurl variable specified in the config file,
simply use the Jinja-like `{{ baseurl }}` tag.

Escaping with backslash is supported. For example if you want to write
`{{ baseurl }}` without having it replaced by the preprocessor, you'll
simply have to write `\{{ baseurl }}`.

## Building juliet websites

Build the website using the `juliet build` command.

`juliet build` builds the website in `build-area` by default. An alternative
destination can be specified using `--build-dst`.

Source directory can also be passed using `--build-src`.

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
