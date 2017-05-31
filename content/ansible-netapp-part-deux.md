Title: Ansible + NetApp: Part Deux
Date: 2016-11-01 19:39
Author: Jeorry Balasabas
Category: DevOps
Tags: ansible, automation, cm, devops, netapp
Slug: ansible-netapp-part-deux
Status: published
Summary: The second part to a series on using Ansible with NetApp cDOT arrays.

I promised to dig a little deeper into what you can do with Ansible and
NetApp in my last post. In the spirit of 30 blog posts in 30 days I
decided to cheat a little on the first post by counting this as \#1.
Without further ado let's jump right in to the good stuff.

How many times have you had to create multiple volumes, LIFs, etc. and
you pop open Excel to create a concatenate formula and copy and paste
into your terminal emulator of choice? Ansible allows you to accomplish
this using the built in "with\_items:" statement. Consider the following
task of creating several LIFs.
    
    :::yaml
    - name: Create lif 1 for nfs
        int_create:
          cluster: "192.168.0.1"
          user_name: "admin"
          password: "Password1"
          vserver: "svm_nfs"
          lif: "lif_nfs_01"
          role: "data"
          data_proto: "nfs"
          node: "atlcdot-01"
          port: "e0d"
          ip: "192.168.1.178"
          netmask: "255.255.255.0"
    - name: Create lif 2 for nfs
        int_create:
          cluster: "192.168.0.1"
          user_name: "admin"
          password: "Password1"
          vserver: "svm_nfs"
          lif: "lif_nfs_02"
          role: "data"
          data_proto: "nfs"
          node: "atlcdot-01"
          port: "e0d"
          ip: "192.168.1.179"
          netmask: "255.255.255.0"
    - name: Create lif 3 for nfs
        int_create:
          cluster: "192.168.0.1"
          user_name: "admin"
          password: "Password1"
          vserver: "svm_nfs"
          lif: "lif_nfs_03"
          role: "data"
          data_proto: "nfs"
          node: "atlcdot-01"
          port: "e0d"
          ip: "192.168.1.180"
          netmask: "255.255.255.0"


Now the same tasks using "with\_items:"

    :::yaml
    - name: Create lif for nfs
        int_create:
          cluster: "192.168.0.1"
          user_name: "admin"
          password: "Password1"
          vserver: "svm_nfs"
          lif: {{ item.name }}
          role: "data"
          data_proto: "nfs"
          node: "atlcdot-01"
          port: "e0d"
          ip: {{ item.ip }}
          netmask: "255.255.255.0"
        with_items:
          - { name: 'lif_nfs_01', ip: '192.168.0.178' }
          - { name: 'lif_nfs_02', ip: '192.168.0.179' }
          - { name: 'lif_nfs_03', ip: '192.168.0.180' }


As you can see, the task is cleaner and shorter. Now what if we had a
dictionary of LIF names and their respective home nodes, home ports,
vservers and ip addresses that we wanted to loop over in our playbook.
That would be accomplished using the "with\_dict:" statement. Say we had
our dictionary in the following variable file.

    :::yaml
    ---
    lifs:
      lif_cifs_01:
        vserver: svm_cifs
        proto: cifs
        home_node: node1
        home_port: e0c
        ipaddr: 192.168.0.210
      lif_nfs_01:
        vserver: svm_nfs
        proto: nfs
        home_node: node2
        home_port: e0d
        ipaddr: 10.0.0.100


We could loop through this dictionary using "with\_dict:" in our
playbook as follows:

    :::yaml
    - name: Create lifs
        int_create:
          cluster: "192.168.0.1"
          user_name: "admin"
          password: "Password1"
          vserver: {{ item.value.vserver }}
          lif: {{ item.key }}
          role: "data"
          data_proto: {{ item.value.proto }}
          node: {{ item.value.home_node }}
          port: {{ item.value.home_port }}
          ip: {{ item.value.ipaddr }}
          netmask: "255.255.255.0"
        with_dict: "{{ lifs }}"


Hopefully these tips can save you some time with your own playbooks. For
more information about loops in Ansible I recommend the
Ansible [documentation](https://docs.ansible.com/ansible/playbooks_loops.html#).

 
