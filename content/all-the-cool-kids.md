Title: All the cool kids are doing it...
Date: 2017-06-01
Author: Jeorry Balasabas
Category: Python
Tags: Python, Pelican, Github, Markdown
Slug: all-the-cool-kids
Status: draft
Summary: An adventure in migrating my blog from Wordpress to a static site hosted on Github Pages.


I finally succumbed to the peer pressure. After I noticed all the cool kids were moving their blogs to static sites, I decided to take the plunge. I could have gone the easy route and just created a blog on github pages with some of their templates but I wanted to geek out a little bit more. This won't be a how-to guide on static site generators. There are already plenty of guides out there. I suggest starting with the SSG section of Matt Makai's excellent [Full Stack Python](https://www.fullstackpython.com/static-site-generator.html). Instead, I wanted to provide some tips and lessons learned from my experience.

## Why

* I wanted to write my posts in a format that was simple and could be done from any text editor. In my case that meant Markdown.

* Version control for my source content as well as the generated output.

* I absolutely abhorred having to log into my Wordpress admin site just to write a simple article. The more I could get out of my own way the more content I can produce.

## Package Mgmt.
If you only take away one thing from this article it's this. Please use Conda package manager when installing Python packages. I know that most documentation has you using pip to install packages but one of pip's biggest drawbacks is it doesn't track dependencies for non-python packages. Since the ability to import Wordpress xml files relies heavily on parsers that aren't part of the python ecosystem pip has no way of knowing if these packages are compatible or even installed in the first place. I'll say it again. If you want to save yourself hours of banging your head against the keyboard, use conda. For a more in-depth comparison of pip and conda check out [@jakevdp](https://twitter.com/jakevdp)'s excellent [post](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/).

## Pelican
I decided to use Pelican to generate my static site. The biggest reason for me was that it was written in Python. If you decide to use Pelican as well you might be wondering why there is a pelicanconf.py **AND** a publishconf.py file. Both files are utterly the same except one is used for dev/test and the other is used when generating your site for production. The biggest reason for keeping them separate which I could find is that you typically don't want feed generation or plugins like comments or google analytics in your dev environment.

## Github Pages
I decided to use Github Pages because I'd eventually like to use some sort of automation (TravisCI) to automatically publish articles to my site everytime I push with git. Github Pages uses Jekyll behind the scenes so there is a tweak to let Github know that I didn't use Jekyll to build my site. Create a empty file called '.nojekyll' and place it in the following path 'content/extra'. The folder structure would look similar to what's below.

+-- content  
|+---- extra  
|+---------.nojekyll
 

