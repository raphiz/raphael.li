---
title: Custom DDNS Service Provider
tags: synology
date: 2015-03-07
---

The [Synologys DSM operating system](https://www.synology.com/en-us/dsm/) allows you to configure [dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS) in a very simple way. The problem is that most of the listed provides do not suit well for private users. I tried most of the built-in ones. All of them want you to log-in once every month (DynDNS or noip to name just two of them) or to pay a ridiculous amount of money.
Meanwhile, I stumbled over a nice service called [nsupdate.info](https://www.nsupdate.info/). It's simple, free, open source and awesome!

I tried to add custom dynDNS providers directly in system configuration files - which worked but was overridden on almost every update. The built-in updater does also have another drawback: The DynDNS demon notifies the service provider every night which might triggers an abuse alert.

There is a simpler solution! Please note that this article assumes that you use nsupdate.info as dynamic dns provider. However, you should be able to adapt this easily for other service providers.

If not yet done, create a new account on [nsupdate.info](https://www.nsupdate.info/) and register a new host. Save the secret for later use.

{% image "./001.png", "Get the secret from nsupdate" %}

Next, download the following script and modify the two variables on top. `DOMAIN` is your full nsupdate domain name and `TOKEN` is the secret that you saved before.

```bash
#!/usr/bin/env sh

DOMAIN="domain.nsupdate.info"
TOKEN="MYTOKEN"

# Evaluate the current remote IP and the one that is currently registered
CURRENT=$(curl -s https://ipv4.nsupdate.info/myip)
SAVED=$(python2 -c "import socket; print socket.gethostbyname('$DOMAIN')")
LOGFILE=$( cd "$( dirname "${0}" )" && pwd )/log.txt
TEMPFILE=$( cd "$( dirname "${0}" )" && pwd )/tmp

# Write the current date, ip and registered ip into the log file
if [  ! -e "" ]; then
    touch "$LOGFILE"
fi
{
    echo '----------------------------'
    date
    echo "The current external IP is: $CURRENT"
    echo "The following IP is registered: $SAVED"
} >> "$LOGFILE"

# Check if an update is required - if so, update and verify the response
# On the first of every month, update anyway
if [ "$CURRENT" != "$SAVED" ] || [ "$(date +%d)" -eq "01" ]; then
    echo "updating..." >> "$LOGFILE"
    RESPONSE=$(curl --user "$DOMAIN":"$TOKEN" https://ipv4.nsupdate.info/nic/update)
    START=$(python2 -c "print '$RESPONSE'[:5]")
    if [ "$START" = " good" ]; then
        echo "Update successful!" >> "$LOGFILE"
    elif [ "$START" = "nochg" ]; then
        echo "WARNING: ip has not changed - cache" >> "$LOGFILE"
    fi
else
    echo 'no update required' >> "$LOGFILE"
fi

# Keep the log down to 100 lines
cp -R "$LOGFILE" "$TEMPFILE"
tail -n 100 tmp > "$TEMPFILE"
rm "$TEMPFILE"
```

Having that done, it's time to move the script on the synology box. This can in any folder - I called my one `scripts`.

Now let's login on the web interface, open the control panel and select `Task Scheduler`. Create a new `User-defined script`. Give it a name and provide the path to your script. Note that this might differ depending on your setup.

{% image "./002.png", "Create a new User-defined script in the Synology web interface" %}

Choose how often the script is called in the `schedule` tab - I chose to do it twice a day. Save it afterwards.

It's time to test. Select the newly created task in the list and click on `run`. When it's done, open the folder where you placed the script where you will find a file called `log.txt`. It's content should be similar to this:

```text
----------------------------
Mon Jun  1 12:01:30 CEST 2015
The current external IP is: X.X.X.X
The following IP is registered: X.X.X.X
no update required
```

That's all, have fun!
