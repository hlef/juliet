# Juliet *- basics*

**WiP, some features mentioned here may still be in development stage !**

## File structure

Juliet uses the following file structure:

    .config.yml

    index.html

    posts/
    pages/
    statics/
    assets/ <- images, documents, etc.
    themes/ <- themes file structure will be explained later
        | yourtheme/
        | anothertheme/
        ...

`juliet init` initializes this file structure in the current directory.

### The configuration, *config.yml*

`config.yml` is the configuration file of your website. It defines *variables*
needed by the build system, the theme, and static pages.

In general, config files should define at least the following variables since
they are required by the build system:

    # where the website is going to be built
    build-directory: "/srv/blog"

    # useful when your website isn't located at the root of your server
    baseurl: ""

    # the directory in themes/ that contain your theme
    theme: sample

The set of required entries in the configuration file may vary depending on the
theme you are using. You can find more informations about it in your theme
directory, said under `themes/your_theme/README`.

For instance, the *boots* theme requires the following configuration variables:

    TODO

### Blog posts under *posts/*

Juliet supports Markdown articles in the original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax). Articles go in the
`posts/` directory.

### Site pages under *pages/*

Pages should also be written in Markdown. Pages go in the `pages/` directory.

### Static pages under *statics/*

### Some words about themes

## Building the website

Build the website using the `juliet build` command.
