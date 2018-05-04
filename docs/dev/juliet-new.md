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

In the most simple and common case, you would probably call `juliet new --
title = "Title of the article"` to generate a new article, and Juliet would
generate `posts/{current date}-title-of-the-article.md` with the following
content:

```
---
title: "Title of the article"
date: {current date} {current time}
---
```

## Customization

### File name format

Juliet is designed to be as modular as possible. That's why you are free to
choose the file name format you want if you want to change it.

By default, the file name format is `{current date in YYYYMMDD format}-{slugified
article title}.md` for articles and `{slugified page title}.md` for pages.

This can be changed by the user in the `config.yml` file with the
`post-filename-format` and `page-filename-format` entries.

The value should be formatted as following: **TODO**.

### Default entries set

By default, generated articles will only contain `title` and `date` header
entries. This behavior can be changed themewise by defining `.cfg/.newpost.yml`
and `.cfg/.newpage.yml`. These YAML formatted files specify the different
entries to include, whether they are mandatory or not, and if not, what default
value to use or, if applicable, how to generate it. Entries defining no fallback
value will simply not be included.

The required format is:

```
mandatory_fields:
    - entry

optional_fields_val:
    - entry: string value

optional_fields_func:
    - entry : function
```

For example:

```
mandatory_fields:
    - title

optional_fields_val:
    - archived: "false"

optional_fields_func:
    - date : get_current_date
```

Available generator functions will later be specified in a public API. It will
be possible to extend this set of function via a plugin system.

If mandatory arguments didn't get passed via command line arguments after `--`,
Juliet will either fail or interactively ask the user to enter them. This is why
you shouldn't specify too many mandatory args.
