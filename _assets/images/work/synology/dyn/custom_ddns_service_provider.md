# Custom DDNS Service Provider for the Synology DSM
[Synologys DSM operating system](https://www.synology.com/en-us/dsm/) allows you to configure [dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS) in a very simple way. The problem is that most of the listed provides suck for private users. I tried most of them and they all want you to log-in once every month (DynDNS or noip to name just two of them) or to pay them a ton of money.
Recently, I stumbled over a nice service called [nsupdate.info](http://nsupdate.info/). It's simple, free, open source and awesome!
Great, so let's add this to the Synology DSM!

# Let's do it!
There are two files that should be modified on the filesystem to add a new DDNS provider: `/etc/ddns_provider.conf` and `/etc.defaults/ddns_provider.conf`. You can do this by logging in via SSH and use VI or use tools like [Config File Editor](http://www.mertymade.com/syno/#cfe).

All you have to do is to append the following configuration to both of the above mentioned files:

```
[nsupdate]
modulepath=DynDNS
queryurl=ipv4.nsupdate.info/nic/update?hostname=__HOSTNAME__&myip=__MYIP__&system=dyndns&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG
```
Please be advised that this is IPv4 only! (Btw. I just copied the DynDNS section and replaced the hostname in the queryurl because nsupdate is dyndns2 compatible)

`nsupdate` will now show up in the list of available DDNS providers. You can now click `add` in `External Access -> DDNS` and configure nsupdate service provider.
![Nsupdate shows up in DDNS list](img_ddns/002.png)

__The password to be used is not your nsupdate password!__ You can get the password/token from the nsupdate website. It's called a `Generated Host Secret` and is presented to you after adding a new host. It is regenerated when clicking on the `Show Configuration` Buttton on the host dashboard.
![Nsupdate shows up in DDNS list](img_ddns/004.png)

After configuring your new DDNS provider settings, the `Status` section should display `Normal` (or similar). You can also verify if everything worked by visiting nsupdate's dashboard:
![The dashboard displays the last refresh timestamp](img_ddns/001.png)
![The dashboard displays the last refresh timestamp](img_ddns/003.png)

If you want to script this procedure, you can also override the `/etc/ddns.conf` and `/etc.defaults/ddns.conf`  which contains the configuration of your DDNS provider:
```
#If you want to change DDNS Name, remember to change upnpd.c
#  , remember to consider updating problem.
[nsupdate]
hostname=mydomain.nsupdate.info
passwd=Top secrit!
net=DEFAULT
status=
ip=00.00.00.00
service=true
username=mydomain.nsupdate.info
enable_heartbeat=no
provider=nsupdate
ipv6=0:0:0:0:0:0:0:0
```

# The downside
Almost every update overrides the modified files, so you have to do this after almost EVERY update...thank you for this Synology!
![Missing NSupdate config after a patch version update](img_ddns/005.png)
I wrote a shellscript that I run after every update...
I just hope synology will fix this soon.

Let me know if you have any trouble with this!

Happy hacking!
