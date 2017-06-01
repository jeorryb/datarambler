#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jeorry Balasabas'
SITENAME = 'DataRambler'
SITEURL = 'https://www.datarambler.com'
THEME = 'themes/pelican-bootstrap3'
TYPOGRIFY = True
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
PLUGINS = ['i18n_subsites', 'ipynb.markup']
PLUGIN_PATHS = ['plugins']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
PATH = 'content'
DISPLAY_CATEGORIES_ON_MENU = False
BOOTSTRAP_THEME = 'simplex'
BOOTSTRAP_FLUID = True
BANNER = 'images/graph_banner.jpg'
TWITTER_USERNAME = '@jeorryb'
TWITTER_WIDGET_ID = 'jeorryb'
MARKUP = ('md', 'ipynb')


TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll


# Social widget
SOCIAL = (('github', 'https://github.com/jeorryb'),
          ('twitter', 'https://twitter.com/jeorryb'),
          ('linkedin', 'https://www.linkedin.com/in/jeorry'))
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
STATIC_PATHS = ['extra/robots.txt', 'images', 'extra/favicon.ico', 'extra/CNAME', 'extra/.nojekyll']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/.nojekyll': {'path': '.nojekyll'}
}