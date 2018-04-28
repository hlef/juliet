[![Build Status](https://travis-ci.org/hlef/juliet.svg?branch=master)](https://travis-ci.org/hlef/juliet)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.txt)

# Juliet

Juliet is a powerful (yet experimental :D) static websites generator written in
Python. It is designed to be as lightweight and understandable as possible.

Juliet is easily adaptable, forkable, and provides all functionalities a modern
static websites generator should provide.

Some examples of what Juliet can:
 * modular theming with Jinja2 templates
 * markdown articles and pages with Pygments syntax highlighting
 * easy configuration in YAML syntax

## Examples

Some sites using Juliet:

 * [Hugo's Haunt](https://www.owl.eu.com), *[boots](https://github.com/hlef/juliet-boots-theme)* theme

## Dependencies

Juliet requires Python **>= 3.3** to work properly ([why](http://jinja.pocoo.org/docs/2.9/faq/#why-is-there-no-python-2-3-2-4-2-5-3-1-3-2-support)).

Additionally, Juliet requires following dependencies (Debian dependencies in
brackets):

 * [Jinja2](http://jinja.pocoo.org/) , version >= 2.8 (python3-jinja2)
 * [pyyaml](https://github.com/yaml/pyyaml), version >= 3.12 (python3-yaml)
 * [python-markdown](https://github.com/waylan/Python-Markdown), version >= 2.6.8 (python3-markdown)
 * [python-slugify](https://github.com/un33k/python-slugify), version >= 1.2.1 (python3-slugify)
 * [Pygments](http://pygments.org/), version >= 2.2.0 (python3-pygments)

You may also need to install [setuptools](https://github.com/pypa/setuptools) to
use Juliet's setup program.

Required for tests:

 * [nose](https://github.com/nose-devs/nose), version >= 1.3.7 (python3-nose)

## Markdown implementation

Juliet uses the [python-markdown](https://github.com/waylan/Python-Markdown) library for Markdown parsing. It is based on the
original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax).

Juliet has been implemented so that it doesn't really *depend* on the Markdown
implementation. Changing it is quite simple if you want to use Kramdown, for example.

## Contributing

* Release blockers and improvements ideas are in `TODO`
* Design themes for Juliet, and add it in `docs/recommended-themes.md` !
* You are using Juliet ? Add a link to your website here !

Bugs reports and pull-requests are welcome ! :smile:
