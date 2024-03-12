---
title: Custom keyboard layout
tags: linux
date: 2016-06-13
---

I love the US keyboard layout for programming - but because I live in Switzerland I have
to write german texts from time to time.

The german umlauts ä,ö and ü are not present in the standard US keyboard layout.
There is a US-International keyboard layout which actually has these keys on it. However,
they are not located very convenient - the ä for example is mapped to `Alt Gr` + `Q`
whereas on the (Swiss) German keyboard layout it is located next to enter.

It would be impossible to ever use a Swiss German keyboard again if I would train myself to the US international keyboard layout. I therefore had the idea, to tweak the US keyboard like this:

{% image "./xkb_us_umlauts.svg", "My custom keyboard layout" %}

(Modifications in blue - based on ["English: United States keyboard layout
" via Wikimedia Commons](https://commons.wikimedia.org/wiki/File%3AKB_United_States-NoAltGr.svg).)

OK, let's do this!

In most Linux desktop environments, the magic of keyboard layouts happens in [xkb - the X Keyboard Extension](https://www.x.org/wiki/XKB/).

The key maps are located in individual files - usually in `/usr/share/X11/xkb/symbols/`.

After reading in the xkb docs, I understood enough of the configuration format. I copied the US keyboard and replaced the definitions of the affected keys with my customized versions and put
it into a file called `/usr/share/X11/xkb/symbols/us_umlauts`.

```text
// [...]
key <AC10> {	[ semicolon,	colon,		odiaeresis,	Odiaeresis	]};
key <AC11> {	[ apostrophe,	quotedbl,	adiaeresis,	Adiaeresis	]};
key <AD11> {	[ bracketleft,	braceleft,	udiaeresis,	Udiaeresis	]};
// [...]
```

[Checkout this gist for the full us_umlauts file](https://gist.github.com/raphiz/f48f7062f6ff51cdc34d629bc24063cc)

Finally, I had to set it as default keyboard layout for the X-server - which can be
achieved by editing the file `/etc/X11/xorg.conf.d/00-keyboard.conf` and set the option `XkbLayout`:

```text
Option "XkbLayout" "us_umlauts"
```

[Checkout this gist for my 00-keyboard.conf file](https://gist.github.com/raphiz/a239e372021a9d218d386b74c843ea1b)

After I logged out and in again, everything worked as expected - at least since I use Xfce.

Before using Xfce I used Gnome 3 - and Gnome does it's own magic with keyboard layouts.
I could not yet figure out a permanent solution for Gnome - but if you
do, let me know!

## A Note on Windows

It is possible to create custom keyboard layouts on Windows as well (this is especially useful if you are in the habit of using a customised layout).

Download the free tool from Microsoft called [Keyboard Layout Creator 1.4](https://www.microsoft.com/en-us/download/details.aspx?id=22339).
I find the software not intuitive at all - but you can test and see the result immediately. When you're done, build a setup package and install it. This solution is quite nice since it allows you to backup and reuse the setup package on any other Windows PC.

You can also download [my configuration](./en_rz.klc) or [the installer](./en_rz.zip) for my customised layout (both without warranty!).
