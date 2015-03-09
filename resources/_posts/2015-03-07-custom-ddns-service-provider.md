---
layout: post
title: Custom DDNS Service Provider
tags: synology
---
The [Synologys DSM operating system](https://www.synology.com/en-us/dsm/) allows you to configure [dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS) in a very simple way. The problem is that most of the listed provides do not suit well for private users. I tried most of those that are built-in to DSM. All of them want you to log-in once every month (DynDNS or noip to name just two of them) or to pay them a ton of money.
Meanwhile, I stumbled over a nice service called [nsupdate.info](http://nsupdate.info/). It's simple, free, open source and awesome!

## Let's get started
There are two files that must be modified on the file system to add a new DDNS provider: `/etc/ddns_provider.conf` and `/etc.defaults/ddns_provider.conf`. You can do this by logging in via SSH and use VI or use tools like [Config File Editor](http://www.mertymade.com/syno/#cfe). I encourage you to use the latter.

All you have to do is to append the following configuration to both of the above-mentioned files, no modifications required.

```ini
[nsupdate]
modulepath=DynDNS
queryurl=ipv4.nsupdate.info/nic/update?hostname=__HOSTNAME__&myip=__MYIP__&system=dyndns&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG
```

Please be advised that this works with IPv4 only! (Btw. I just copied the DynDNS section and replaced the hostname in the queryurl because nsupdate is dyndns2 compatible)

`nsupdate` will now appear in the list of available DDNS providers. Click `add` in `External Access -> DDNS` and configure the new service provider.

{% image resources/synology/dyn/002.png %}

__Note that the required password is not your nsupdate password!__ You can get the password/token from the nsupdate website. It's called a `Generated Host Secret` and is presented to you after adding a new host. It is regenerated when clicking on the `Show Configuration` button on the host dashboard.

{% image resources/synology/dyn/004.png %}

After configuring the DDNS provider settings, the `Status` section should display `Normal` (or similar). You can also verify if everything worked by visiting nsupdate's dashboard

{% image resources/synology/dyn/001.png %}
{% image resources/synology/dyn/003.png %}

If you want to script this procedure, override the `/etc/ddns.conf` and `/etc.defaults/ddns.conf` which contains the configuration of your DDNS provider.

```ini
#If you want to change DDNS Name, remember to change upnpd.c,
#remember to consider updating problem.
[nsupdate]
hostname=mydomain.nsupdate.info
passwd=Top Secret!
net=DEFAULT
status=
ip=00.00.00.00
service=true
username=mydomain.nsupdate.info
enable_heartbeat=no
provider=nsupdate
ipv6=0:0:0:0:0:0:0:0
```

## The downside
DSM Updates might break this! It's unclear to me why updates override both `ddns_provider.conf` files.
You can detect this if the `External Access -> DDNS` displays neither a service provider nor a status.

{% image resources/synology/dyn/005.png %}

Let's hope Synology fix this soon.

Happy hacking!
