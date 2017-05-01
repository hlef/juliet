# Juliet

Juliet is a powerful (yet experimental :D) static websites generator written in
Python. It is designed to be as lightweight and understandable as possible.

Juliet is easily adaptable, forkable, and provides all functionalities a modern
static websites generator should provide. It uses Jinja2 templates, supports
modular theming, markdown articles with Pygments syntax highlighting and is
easily configurable via YAML configuration files.

## Dependencies

Juliet requires following dependencies to work properly (Debian dependencies in brackets):

 * [Jinja2](http://jinja.pocoo.org/) , version 2.8 (python3-jinja2)
 * [pyyaml](https://github.com/yaml/pyyaml), version 3.12 (python3-yaml)
 * [python-markdown](https://github.com/waylan/Python-Markdown), version 2.6.8 (python3-markdown)
 * [python-slugify](https://github.com/un33k/python-slugify), version 1.2.1 (python3-slugify)
 * [Pygments](http://pygments.org/), version 2.2.0 (python3-pygments)

Required for tests:

 * [nose](https://github.com/nose-devs/nose), version 1.3.7 (python3-nose)

## Markdown implementation

Juliet uses the python-markdown library for Markdown parsing. It is based on the
original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax).

Juliet has been implemented so that it doesn't really 'depend' on the Markdown
implementation, and it is very easy to change it if you want to use Kramdown,
for example.

## Contributing

Bugs reports and pull-requests are welcome ! :smile:
