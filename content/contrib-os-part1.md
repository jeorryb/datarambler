Title: Contributing to Open Source Projects: Part 1
Date: 2017-06-01
Author: Jeorry Balasabas
Category: Python
Tags: Python, Cisco, Github, 
Slug: contrib-opensource-part1
Status: draft
Summary: Giving back to the Open Source community we all know and love


Lately, I've been working on automating parts of Cisco's UCS platform. Luckily Cisco published their Ansible modules on Github. Digging through the modules you quickly discover that the modules require the ucsmsdk which provides a low level framework for dealing with UCS programatically. They also require the UCSM API which happens to be written in Python and is a higher level framework meant to make it easier to deal with UCS. Unfortunately, there happens to only be a small set of modules written for the API. I've always thought that more people would contribute or help but they just don't know where to start. My hope with this series is to take you from zero to github contributor hero in no time.

My plan isn't to re-write steps which others have already so eloquently explained but rather to fill in the missing blanks. If you don't already have git installed then lets go ahead and get it loaded. I know from experience that git can be a little intimidating at first so I've included some resources below that I found very helpful.

