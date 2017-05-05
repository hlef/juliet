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

### The configuration, *config.yml*

`config.yml` is the configuration file of your website. It defines *variables*
needed by the build system, the theme, and static pages.

In general, config files should define at least the following variables since
they are required by the build system:

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

Posts go in the `posts/` directory.

### Site pages under *pages/*

Pages follow the exact same template as posts and go in the `pages/` directory.

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
    ├── statics
    │   ├── index.html
    │   └── ...
    └── templates
        ├── pages.html
        ├── posts.html
        └── ...

## Building the website

Build the website using the `juliet build` command. It will build the website
in `build-area`. Alternatively, you may want to specify a destination using
`--build-dst`.

You can also specify the source directory via `--build-src`.
