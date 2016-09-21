---
layout: post
title: Put your OS into a Virtual Box
tags: linux
---

Have you ever wanted to (re-)install an operating system but are afraid to forget backing up something? Or maybe you backed up everything but forgot the name of that tool you had installed before? Then stop worry - and read on!

Soon, I'll get a new notebook - an ideal opportunity to set up a new and clean system. I had all of the above-mentioned problems before. What annoys me most, however, are dot-files. Because I don't keep track of them meticulously, things get messy after some time. I'm glad when the number of hidden directories in my home directory drops significantly after a clean installation - but I don't want to delete them - just in case.

Some would argue - well then just back it all up! Yes - that's what I'm going to do - but even better! I'll convert the barebone installation into a Virtual Machine; so I can boot my good old system whenever I want to check these neat tweaks from past days.

## Requirements
i
To get this going, I needed ...

* ... a lot of time  - most of it for copying
* ... a running VirtualBox installation (on the target system)
* ... lots of external storage (>= the size of your harddisk)
* ... some Linux command line knowledge

## Let's do this!

### Boot from a live distribution

In my case, I used the latest (Manjaro XFCE)[https://manjaro.github.io/] image because that's the distribution I use - but any other distribution should get the job done.

### Backing up
Time to save all that precious bits! I fired up a shell and dumped the entire disk into a single file on my external harddrive.

```bash
cd /path/to/external/harddist/
dd if=/dev/sda of=./dump.raw
```
(Note that `/dev/sda` might differ on your machine. Also be sure to backup the whole disk (`sda`) and not just some partitions such as `sda1` or `sda2`

### Boot the target system
The bits are safe - but in the wrong format. VirtualBox prefers the vid file format. The conversion isn't complicated, but it takes way too much time!

Note that it *might* be possible to pass the dump from before directly to VirtualBox. If so, lucky you! It's worth trying to skip this step - but if you can't boot in the next step do the conversion.

```
sudo VBoxManage convertdd dump.raw sda.vdi --format VDI --variant Fixed
```

### Creating the VM
After a good night sleep, the conversion completed. The data is ready so let's create a new VM (Click on "New")

I choose the arch template and did not specify the harddisk in the setup wizard. Next, I open the VM settings and change the following settings:

    * General -> Advanced -> Shared Clipboard: Bidirectional
    * General -> Advanced -> Drag'n'Drop : Bidirectional
    * System -> Motherboard -> Base Memory: ~ 50% of your Memory
    * Display -> Screen -> Video Memory: As much as Possible
    * Display -> Screen -> Enable 3D Acceleration: Checked
    * Storage: Right click in the Storage Tree, Select "Add SATA Controller"
    * Storage: Click on the Harddisk Symbol of the SATA Controller, click on `Choose existing disk` and select the vid image

### Try it out!
Ready for takeoff :rocket:
Start the VM and watch... Boom! The system booted. The graphical interface ... didn't. That's because graphic cards and Linux is a horror story.

On Manjaro, it was pretty easy to find a suitable driver...

```bash
mhwd -a pci free 0300
```

...and installing  the virtualbox guest utils

```bash
pacman -Ss virtualbox-guest-utils virtualbox-guest-dkms
```
After that - thaddaa!


## Using KVM
You can save a lot of time by using KVM with virt-manager instead of VirtualBox.
KVM can read raw images directly - which saves you the painful conversion time.

However, You have to consider the following aspects:
* Change the Disk Bus (??) from VirtIO to Sata
* Eventually Set a specific UUIDi
* Setup a shared folder to transfer data between the guest and the host
* [Resize the Partition](https://help.ubuntu.com/community/ResizeEncryptedPartitions)
