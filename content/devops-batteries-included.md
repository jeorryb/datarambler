Title: DevOps: Batteries Included
Date: 2017-02-24 16:40
Author: Jeorry Balasabas
Category: DevOps
Tags: ansible, automation, devops, Docker, netapp, Python
Slug: devops-batteries-included
Status: published
Summary: Introduction to using Docker to wrap ansible modules and NetApp's NMSDK to 'toolify' a dev environment.

When I first started building Ansible modules I didn't give any thought
to what environments others would be using them in. In a perfect
world you would have your config mgmt. and automation framework set up
and running without any issues in 5 minutes. Now in certain
environments (\*NIX) that is true. But there are still others that are
running environments on Windows (I can't look at you) or OSX or whatever
OS you happen to be running. In that case, consuming Ansible custom
modules or playbooks plus certain python libraries (NetApp's
Manageability SDK) can be difficult, especially for beginners. When I
realized how difficult it would be for some to take advantage of Ansible
and all of its goodness I started searching for an easy button.

Docker to the rescue.
---------------------

![Docker Whale]({filename}/images/docker_whale.png)

Instead of leaving beginners out in the cold, the only onus on you is to
get docker installed and the Dockerfile provides the rest. I wasn't able
to cut out all the manual steps for certain reasons that I'll explain
below but I've simplified it as much as I can. Once you’ve built your
Docker image, you’ll be able to run Ansible playbooks using custom
modules in one line.

I want to thank [Andrew
Sullivan](https://netapp.github.io/authors/andrew-sullivan) for his post
on adding NMSDK to Docker and [Phil
Misiowiec](https://github.com/philm) for his ansible\_playbook image
from which I heavily borrowed.

You can grab the Dockerfile to build an image
[here](https://github.com/jeorryb/netapp-ansible). I decided not to
package the NMSDK in my github repo for fear of licensing repercussions
from NetApp. If you are a NetApp customer or partner then you have the
ability to download the nmsdk for free. Since I’m assuming most
consumers of this Dockerfile will be customers or partners then I don’t
feel guilty for not providing it in the image itself.

I also included the path to my github repo where the custom ansible
modules are located. If you ever want the latest modules you're only one
docker build command away. The following is from the Dockerfile.

    :::go
    RUN git clone https://github.com/jeorryb/netapp-ansible.git /github

Once you’ve downloaded the nmsdk place it in the same directory that
your run your docker build command from.

    :::bash
    docker build -t ansible-nmsdk .

Adventures in certificate hell.
-------------------------------

**SSL: CERTIFICATE\_VERIFY\_FAILED**

The other manual process that I included involves trusting the self
signed cert from the cdot array that you are executing against. When I
started building modules for cdot I made the decision to use https for
connectivity to the array. At the time, I had no idea the rabbit hole
that I was about to venture into. If you’ve ever made SSL calls from
Python and received the exception above, you know what I’m talking
about.

> **The "S" in "HTTPS" stands for secure.**

Since I decided to use SSL for my NMSDK calls, I had to either apply
certs signed from a trusted CA to my cluster or download the self signed
certs that cdot creates when creating a cluster. I went with downloading
the existing self signed cert and I’m guessing most will take that route
as well. For a comprehensive explanation of Python and SSL checkout [PEP
476](https://www.python.org/dev/peps/pep-0476/). The following is an
example of running a Ansible playbook as a one liner with Docker.

    :::bash
    docker run -it -v $(pwd):/etc/ssl/certs -v /Users/jeorryb/images/ansible_nmsdk:/ansible/playbooks ansible-nmsdk nmsdk.yaml

In the above command I’m mounting two volumes from my local host
to the container. The first mount is my present working directory 
where I’ve downloaded the cert from my cluster. Mounting the cert
location on my host to the trusted certificate location on the container is a neat
little trick to get the container to trust additional certs you have.
The second mount is the directory where my playbook is located. You
don’t have to specify \$(pwd) but I find it easier for one of the
mounts. In the command above “ansible-nmsdk” is the name I gave to my
Docker image and “nmsdk.yaml” is the ansible playbook I want to execute.

Hopefully this makes it easier to play around with Ansible and NetApp
and encourages you to include other “batteries” in your Docker images.
