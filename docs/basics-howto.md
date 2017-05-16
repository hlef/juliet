# Juliet *- basics*

**WiP, some features mentioned here may still be in development stage !**

## File structure

A Juliet website is organized as following.

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

Please, note that Juliet won't install a theme in `themes/̀ . You'll have to pick one
somewhere and install it, or design it by yourself (more informations available in
`docs/themes-howto.md`).

We also provide a list of recommended themes in ̀`docs/recommended-themes.md`.

### The configuration, *config.yml*

`config.yml` is the configuration file of your website. It defines *variables*
needed by the build system, the theme, and static pages.

Config files should define at least the following variables since they are
required by the build system:

    # useful when your website isn't located at the root of your server
    baseurl: ""

    # the directory in themes/ that contain your theme
    theme: sample

The set of required entries in the configuration file may vary depending on the
theme you are using. You can find more informations about it in your theme
directory, under `themes/your_theme/README`.

### Blog posts under *posts/*

Juliet posts are divided in two parts.
 * The *header*, containing YAML-formatted informations about the post
 * The post's *body*, in in the original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax)

For example:

    ---
    title: "Hello, world !"
    date: 2016-04-06 16:07:35
    ---

    Hello, **world** !

The set of required entries in post headers may vary depending on the
theme you are using. You can find more informations about it in your theme
directory, under `themes/your_theme/README`.

Posts go to the `posts/` directory.

### Site pages under *pages/*

Pages follow the same header/body structure as posts.

Required header entries should also be defined in the README file of your theme.

pages go to the `pages/` directory.

### Some words about themes

Juliet themes are organized as following:

    .
    ├── data
    │   ├── css
    │   │   └── ...
    │   ├── fonts
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

The most important things:

 * files placed under data/ will be copied as-is to the root directory of your website.
 * files placed at the root of the theme directory are ignored by the build system. Thus,
   `README`, `LICENSE`, `config.yml.EX` are only present for the sake of documentation.

You can find more informations about theming in `docs/themes-howto.md`.

## Building the website

Build the website using the `juliet build` command. It will build the website
in `build-area`. Alternatively, you may want to specify a destination using
`--build-dst`.

You can also specify the source directory via `--build-src`.
