---
layout: post
title: Custom DDNS Service Provider
tags: synology
---
The [Synologys DSM operating system](https://www.synology.com/en-us/dsm/) allows you to configure [dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS) in a very simple way. The problem is that most of the listed provides do not suit well for private users. I tried most of the built-in ones. All of them want you to log-in once every month (DynDNS or noip to name just two of them) or to pay a ridiculous amount of money.
Meanwhile, I stumbled over a nice service called [nsupdate.info](http://nsupdate.info/). It's simple, free, open source and awesome!

I tried to add custom dynDNS providers directly in system configuration files - which worked but was overridden on almost every update. The built-in updater does also have another drawback: The DynDNS demon notifies the service provider every night which might triggers an abuse alert.

There is a simpler solution! Please note that this article assumes that you use nsupdate.info as dynamic dns provider. However, you should be able to adapt this easily for other service providers.

If not yet done, create a new account on [nsupdate.info](http://nsupdate.info/) and register a new host. Save the secret for later use.

{% image resources/synology/dyn/001.png %}

Next, download the following script and modify the two variables on top. `DOMAIN` is your full nsupdate domain name and `TOKEN` is the secret that you saved before.

<script src="https://gist.github.com/raphiz/837453f189dca966a69c.js"></script>

Having that done, it's time to move the script on the synology box. This can in any folder - I called my one `scripts`.

Now let's login on the web interface, open the control panel and select `Task Scheduler`. Create a new  `User-defined script`. Give it a name and provide the path to your script. Note that this might differ depending on your setup.

{% image resources/synology/dyn/002.png %}

Choose how often the script is called in the `schedule` tab - I chose to do it twice a day. Save it afterwards.

It's time to test. Select the newly created task in the list and click on `run`. When it's done, open the folder where you placed the script where you will find a file called `log.txt`. It's content should be similar to this:

```
----------------------------
Mon Jun  1 12:01:30 CEST 2015
The current external IP is: X.X.X.X
The following IP is regitered: X.X.X.X
no update required
```

That's all, have fun!
