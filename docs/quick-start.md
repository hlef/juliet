# Juliet *- workflow*

Ongoing documentation work.

## Initial setup

The following commands will

* initialize a juliet source directory
* create a first blog post
* build the newly created blog to `build-area`

    $ juliet init
    $ juliet new -- title "Going to Mars" author "Opportunity (a.k.a MER-B)" date "July 7, 2003"
    $ echo "\nTo Infinity... and Beyond\!" >> posts/2003-07-07-going-to-mars.md
    $ juliet build --auto-baseurl

Open your new blog in your favourite browser: it works!

    $ firefox build-area/index.html
