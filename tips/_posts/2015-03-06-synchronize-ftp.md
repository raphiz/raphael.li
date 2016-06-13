---
layout: post
title: Synchronize ftp server with a local directory
tags: linux
---

## tl;dr
Install `Unison` and `curlftpfs`. Mount the ftp share using `curlftpfs` and
then perform a simple Unison sync.

For a working example, checkout the script below.

## Why?
I had to do some work on a shared ftp server lately.
Since I also work in trains where the internet connection
can be terribly slow, I like to be able to do work offline.
The easiest solution would have been to just copy the directory to my local machine and later upload my changes. But since I'm not the only one working on this server, conflicts might occur.
Of course, doing collaborative work on a ftp server is a very bad idea!

Anyway, I started to look around for solutions.
I immediately thought of git and figured out that it is possible to push to a ftp remote. This approach, however, fails when it
comes to fetch changes from the server that were not done with git.

I started to think about `rsync`, but `rsync` is focused on one directional synchronizations.

## The solution
The number one recommendation I found for a bi-directional `rsync` alike tool is [Unison](https://www.cis.upenn.edu/~bcpierce/unison/).
`Unison` is one of those tools that are very easy to use and just work out of the box.

I wrote a very basic script that performs a synchronization of a local directory and a remote ftp server.
To get started, we have to install Unison. The set up also requires
`curlftpfs` because `Unison` is not able to sync over ftp.

```bash
$ sudo pacman -S unison curlftpfs # on Arch
$ sudo apt-get install unison curlftpfs # On ubuntu
```

That's all we need - so here is the script:

```bash
#!/usr/bin/env bash
# Requires: curlftpfs, Unison and fuse.


# Configuration:
MOUNTPOINT=/mnt/my_ftp_share/
LOCAL="/home/user/directory"
ftp_HOST="example.com"
ftp_USER="user"
ftp_PASS="secret"
ftp_SUBFOLDER="httpdocs/"


# Mount ftp share
curlftpfs "$ftp_USER:$ftp_PASS@$ftp_HOST" "$MOUNTPOINT"

# Sync and accept defaults
Unison -auto "$MOUNTPOINT/$ftp_SUBFOLDER" "$LOCAL"

# Umount
fusermount -u "$MOUNTPOINT"

```

If you want to exclude files from the sync, add them into the file `~/.Unison/default.prf`


```
ignore = Path {ftp_sync.sh}
```
