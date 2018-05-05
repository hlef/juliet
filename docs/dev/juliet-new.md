# `juliet new` *- development documentation*

This is a development specification of the 0.2 planned `juliet new` feature.
This document is potentially incomplete and subject to change until release.

## Usage

`juliet new` allows one to generate fresh, new, ready to fill article and page
templates in a simple yet modular manner.

```
usage: juliet new {post, page} [-h] [--debug] [--version] [--build-src SRC] -- field:value ...

optional arguments:
  -h, --help            show this help message and exit
  --debug, -d
  --version             show program's version number and exit
  --build-src SRC, -s SRC
                        juliet source directory where to initialize article
```

### Article generation example

`juliet new -- title = "Title of the article"` will generate
`posts/{current date}-title-of-the-article.md` with the following content:

    ---
    title: "Title of the article"
    date: {current date} {current time}
    ---

## Customization

While `juliet new` is designed to work out-of-the-box with a well-specified
default behavior, it is also very customizable, both on user and template
designer sides.

### User: file name format

By default, the file name format is `{current date in YYYYMMDD format}-{slugified
article title}.md` for articles and `{slugified page title}.md` for pages.

This behavior can be easily changed by the user:
 * specify a custom generator function in `.addons/file-name-formatting.py`. The
   interface will be specified later.
 * Set `override-post-filename-format` (or `override-page-filename-format`) to
   true in your `config.yml` to tell Juliet to use these generators instead of
   the default one.

### Theme designer: default entries set

By default, `juliet new` will generate articles templates with `title` and `date`
header entries. This behavior can be changed themewise by defining `.cfg/.postheader.yml`
and `.cfg/.pageheader.yml`. These YAML formatted files specify the different
entries to include, and if applicable, how to generate their value.

The required format is:

    handfilled:
        - entry: fallback value

    generated:
        - entry : function

For example:

    handfilled:
        - title:
        - archived: "false"

    optional_fields_func:
        - date : current_datetime

Available generator functions will later be specified in a public API.

If Juliet doesn't specify the generator functions you need, you can also define
your own ones under `.cfg/.addons/header-generators.py`. The interface will be
specified later.
