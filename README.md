# Source for https://www.datarambler.com

This repository contains the source for https://www.datarambler.com.

## Building the Blog

Clone the repository

```
$ git clone https://github.com/jeorryb/datarambler.git
```

Install the required packages:

```
$ conda create -n pelican-blog python=3.5 jupyter notebook
$ source activate pelican-blog
$ conda install pelican Markdown ghp-import
```

Build the html and serve locally:

```
$ make html
$ make serve
$ open http://localhost:8000
```

Deploy to github pages

```
$ make publish-to-github
```