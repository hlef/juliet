# Juliet *- basics*

**WiP, some features mentioned here may still be in development stage !**

## File structure

Juliet uses the following file structure:

    .config.yml
    posts/
        # your posts
    pages/
        # your pages
    assets/
        # your assets (images, documents, etc.)
    themes/
        theme1/
            # Theme content. We will speak about it later.

You can initialize this file structure by calling `juliet init` in the desired
directory.

Please, note that `juliet init` won't install a theme in your `themes/`
directory. You should pick one on the Internet ([here]() for example) or design
one by yourself (some advices [here]()).

In general, juliet has been designed so that you don't have to understand your
theme to use it.

## Configuration

The required entries in the `config.yml` config file depend on the theme you are
using. In general, config files should define at least the following variables
since they are required by the build system:

    # where the website is going to be built
    build-directory: "/srv/blog"

    # useful when your website isn't located at the root of your server
    baseurl: ""

    # the directory in themes/ that contain your theme
    theme: sample

The variables required by your theme should be listed under `themes/your_theme/README`.

The *boots* theme, for example requires the following configuration variables:

    TODO

## Writing articles

Juliet supports Markdown articles in the original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax). Articles go in the
`posts/` directory.

## Writing pages

Pages should also be written in Markdown. Pages go in the `pages/` directory.

## Building the website

Build the website using the `juliet build` command.
