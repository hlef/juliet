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

`juliet init` can initialize this file structure for you in the current directory.

Please, note that Juliet won't install a theme in `themes/`. You'll have to pick one
somewhere and install it, or design it by yourself (more informations available in
`docs/themes-howto.md`).

We also provide a list of recommended themes in `docs/recommended-themes.md`.

### Build configuration, *config.yml*

`config.yml` is the configuration file of your website. It defines *variables*
needed by the build system, by your theme, and static pages.

Following variables are required by the build system and are thus mandatory for
any Juliet config file:

    # useful when your website isn't located at the root of your server
    baseurl: ""

    # the directory in themes/ that contain your theme
    theme: sample

The set of required entries in the configuration file may vary depending on your
theme. You can find more informations about it in your theme directory, under
`themes/your_theme/README`.

### Blog posts, *posts/*

Juliet posts go to the `posts/` directory and are divided in two parts:
 * The *header*, containing YAML-formatted informations about the post
 * The post's *body*, in in the original [Markdown syntax](https://daringfireball.net/projects/markdown/syntax)

For example:

    ---
    title: "Hello, world !"
    date: 2016-04-06 16:07:35
    ---

    Hello, **world** !

The set of required entries in post headers may vary depending on your theme.
You can find more informations about it in your theme directory, under
`themes/your_theme/README`.

Please, note that even if it is empty, the header has to be present. Otherwise,
Juliet might be upset ! :)

### Site pages, *pages/*

Pages go to the `pages/` directory and follow the same header/body structure as
posts.

Required header entries might be different to the ones required for posts and
should also be defined in the README file of your theme.

### Pygments syntax highlighting

Juliet provides native integration of [Pygments](http://pygments.org/) syntax
highlighting.

To highlight code using Pygments, you'll simply need to embrace your code with
Jinja-like `{% highlight LANG %}` (replace *LANG* by a lexer name) and
`{% endhighlight %}` tags.

For example, highlighting a shell script works as following:

    {% highlight shell %}
    # This is a shell script.
    echo "Hello, World"
    {% endhighlight %}

Escaping with backslash is also supported. For example if you want to include a
`{% endhighlight %}` without having it processed by the preprocessor, you'll
have to write it `\{% endhighlight %}`.

### Base url inclusion

If you want to refer to the baseurl variable specified in the config file,
simply use the Jinja-like `{{ baseurl }}` tag.

This tag can also be escaped: `\{{ baseurl }}`.

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

Most important things:

 * files placed under data/ will be copied as-is to the root directory of your website.
 * files placed at the root of the theme directory are ignored by the build system. Thus,
   `README`, `LICENSE`, `config.yml.EX` are only present for the sake of documentation.

You can find more informations about theming in `docs/themes-howto.md`.

## Building the website

Build the website using the `juliet build` command. It will build the website
in `build-area` by default. Alternatively, you may want to specify a destination
using `--build-dst`.

You can also specify the source directory via `--build-src`.
