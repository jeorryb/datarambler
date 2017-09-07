Title: Veeam + AWS File Gateway: Insurance for Data
Date: 2017-09-07
Author: Jeorry Balasabas
Category: BC/DR
Tags: AWS, Veeam, Backup, DR
Slug: veeam-aws-fg
Status: published
Summary: AWS Storage Gateway options for Veeam backups to the cloud.

> **Everyone has a plan till they get hit in the mouth.**

With Hurricane Harvey still fresh on everyone's mind and Irma bearing down on the Florida Coast we thought it would be appropriate to talk about backups and more importantly offsite backups. Until recently, offsite backups meant costly tape libraries and rotation services or replicating a subset of your primary data center in a colo facility typically located less than twenty miles away. One of the first use cases for cloud infrastructure was for test/dev or backups. It would be nice if Veeam had the ability to back directly up to an S3 bucket, and if I had to put money on it, I have a sneaking suspicion that this feature might be coming in the near future. Until then, we have a few options. I also want to take the time and thank [Taylor Riggan]((https://twitter.com/@triggan) for his help and input on the AWS side of the house.

## AWS Volume Gateway

The first iteration of the AWS Storage Gateway was presented as an iSCSI volume that could be locally mounted as another drive or mount point on your server. In order to utilize the gateway with Veeam you only had to create a new backup repository selecting the iSCSI drive on your server. The storage gateway appliance can be installed as a simple VMware OVA appliance and drives attached to it like you would with any other VM in your environment. A minimum of 2 drives is recommended for the appliance. One drive acts as a local cache for frequently accessed data and the other drive is a buffer for sending data to S3. Benefits of the volume gateway are as follows.

* Can be mounted as a local drive on any server with iSCSI capabilities.

* Utilized by Veeam as a local drive for backup repository

* Supports EBS snapshots.

## AWS Tape Gateway

The second offering of the storage gateway was a Virtual Tape Libary. Similar to the volume gateway the tape gateway is installed as a virtual appliance. Again, it utilizes a cache and buffer drive. If you've ever implemented a backup/DR solution for a client you know how difficult it can be to explain to them how backups work when they aren't used to a tape rotation system. The tape gateway allows enterprises the ability to utilize existing tape backup software as well as fit into an existing tape rotation schedule. The tape gateway brings the following benefits to the table.

* Presented to the Veeam server as an iSCSI tape device.

* Utilize existing backup/tape retention schedule

* Ability to archive virtual tapes to Amazon Glacier

## AWS File Gateway

The latest offering of the storage gateway comes in the form of an NFS file share. AWS presents the S3 bucket through this file system and during backups there is a 1-1 mapping between files and objects. Similar to the Volume Gateway, the File Gateway keeps recently accessed data in a local cache and you have the ability to tier or archive stale data to Glacier. Because Veeam utilizes a proprietary NFS server for VPower features the NFS share must be mounted on a separate server that the main Veeam server. In our testing, mounting the share on a Linux server proved to be the past of least resistance. Additional benefits of the file gateway are as follows.

* Store and retrieve S3 objects through a standard file system protocol (NFS).

* Store frequently accessed data in a local cache.

* Useful for migrating large filesystem to object based storage.

## AWS Setup and Provisioning.

Since there are already plenty of good resources for configuring Veeam to backup to either the Volume or Tape gateway, we thought it would be more helpful to show the configuration for the File Gateway. AWS has a great [Getting Started Guide](https://docs.aws.amazon.com/storagegateway/latest/userguide/GettingStarted.html) on their site. We did want to point out a few gotcha's that we ran into during setup.

* Select the right gateway

I know this might sound simple but at first, we were tempted to use the same ova gateway when we were testing the VTL and File gateway. Depending on what you select, the correct OVA appliance will be presented to download. The OVA name might look similar but they are distinctly different one you've configured them and you try to connect them to your AWS account.

![AWS Gateway Type]({filename}/images/awsgatewaytype.jpg)

* Thick provision cache/buffer disks

AWS recommends thick provisioning the cache and buffer disks because it can affect the performance of the gateway if using Thin Provisioning. During testing, I used thin provisioned disks that were based on thin provisioned NFS datastores on a NetApp array. I didn't see any adverse effects but I could see how latency could become an issue if any link in the chain becomes resource constrained.

* Use Paravirtualized disk controllers on your gateway VM.

AWS requires that the gateway VM use paravirtualized disk controllers. This can be done by editing the settings of the gateway VM.

![Paravirtual]({filename}/images/paravirtual_disk.jpg)


* Create S3 bucket before creating the gateway.

When provisioning the gateway it asks for the S3 bucket where you want to store your files. The S3 bucket MUST already exist and it will not create it for you. You might not have missed this step but it's worth pointing out. Also, since S3 bucket names are in a global namespace, now would be a good time to create any buckets for projects that you want are working on or might work on in the future.

* Mount options.

Once you've created the file share, AWS is kind enough to provide you with the exact command to mount the share on your OS.

![Mount Options]({filename}/images/aws_fg_mount_options.png)

## Veeam Setup and Provisioning

Once the gateway has been deployed and you've mounted it on your Linux host you can configure Veeam to utilize it as a backup repository.

* Linux Server as backup repository

![Veeam Linux Repository]({filename}/images/linux_repo.jpg)

Even though Server 2012 allows you to mount NFS shares we ran into some trouble when getting Veeam to recognize the share as a path that it could back up to. The NFS share mounted on a Linux host worked like a charm and is what we recommend for this type of architecture.

Once the backup repository has been configured you can point any of your Veeam backups to utilize S3 as your offsite storage or archive.

![Veeam Backup Options]({filename}/images/veeam_backup_options.jpg)

We can see this being used as a way to augment your current backup process with offsite backups to the cloud or as a way to provide offsite archiving capabilities without the capital expense of new hardware. Utilizing snapshots as your primary backups and offloading longer retention jobs to S3 through the file gateway provides an extremely efficient and robust backup solution.

