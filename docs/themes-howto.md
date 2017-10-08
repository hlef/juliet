# Juliet *- theming*

## File structure

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

## Files at the root

Files placed at the root of the theme directory are ignored by the build system.
`README`, `LICENSE`, `config.yml.EX`, ... are only present for the sake of
documentation.

## Templates, *templates/*

Juliet uses [Jinja2](http://jinja.pocoo.org/) templates for theming.

Two templates are required by the build system: `pages.html` and `posts.html`.

The build system provides access to a variety of variables:

* `{{ content }}` for the current page/post's content

* `{{ page }}` (array) for the *current* page/post's header, e.g. if current
page/post defines a `title` header entry it can be accessed using `{{ page.title }}`.

* `{{ site }}` (array) for site-wide configuration options defined in `config.yml`.

* `{{ posts }}` (array) containing all posts headers

* `{{ pages }}` (array) containing all pages headers

## Templates inclusions, *includes/*

As defined in the [Jinja2](http://jinja.pocoo.org/) documentation, Jinja
templates may include code snippets. We recommend you to store them under
`includes/`.

For instance `head.html` could be stored as `includes/head.html` and accessed
in `templates/main.html` using `{% include "includes/head.html" %}`.

## Static, theme specific pages, *statics/*

Some pages don't require any template because they are unique, like `index.html`.
`statics/` is the right place to store them.

Static pages follow the exact same rules as normal templates and may even extend
them using, for example, `{% extends "templates/main.html" %}`.

## Resources, *data/*

Files placed under `data/` will be copied as-is to the root directory of your website.

This directory is perfect to include your site-wide ressources, like:

* css files
* fonts
* javascript files
* favicons

so one and so forth.
