# Juliet *- theming howto*

### File structure

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

### Files at the root

Files placed at the root of the theme directory are ignored by the build system.
Thus, `README`, `LICENSE`, `config.yml.EX` and analog are only present for the
sake of documentation.

### Templates, *templates/*

### Templates inclusions, *includes/*

### Static, theme specific pages, *statics/*

### Resources, *data/*

Files placed under `data/` will be copied as-is to the root directory of your website.

This directory is perfect to include your site-wide ressources, like:

* css files
* fonts
* javsacript files
* favicons

so one and so forth.
