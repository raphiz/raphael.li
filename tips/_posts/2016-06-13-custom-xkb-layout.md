---
layout: post
title: Custom keyboard layout
tags: linux
---

I love the US keyboard layout for programming - but because I live in Switzerland I have
to write german texts from time to time.

The german umlauts ä,ö and ü are not present in the standard US keyboard layout.
There is a US-International keyboard layout which actually has these keys on it. However,
they are not located very convenient - the ä for example is mapped to `Alt Gr` + `Q`
whereas on the (Swiss) German keyboard layout it is located next to enter.

It would be impossible to ever use a Swiss German keyboard again if I would train myself to the US nternational keyboard layout. I therefore had the idea, to tweak the US keyboard like this:

<figure>

{% image resources/custom-xkb-layout/xkb_us_umlauts.svg %}

<figcaption>
Modifications in blue - based on <a href="https://commons.wikimedia.org/wiki/File%3AKB_United_States-NoAltGr.svg">"English: United States keyboard layout
" via Wikimedia Commons</a>
</figcaption>
</figure>

OK, let's do this!

In most Linux desktop environments, the magic of keyboard layouts happens in [xkb - the X Keyboard Extension](https://www.x.org/wiki/XKB/).

The key maps are located in individual files - usually in `/usr/share/X11/xkb/symbols/`.

After reading in the xkb docs, I understood enough of the configuration format. I copied the US keyboard and replaced the definitions of the affected keys with my customized versions and put
it into a file called `/usr/share/X11/xkb/symbols/us_umlauts`.

```xkb
// [...]
    key <AC10> {	[ semicolon,	colon,		odiaeresis,	Odiaeresis	]};
    key <AC11> {	[ apostrophe,	quotedbl,	adiaeresis,	Adiaeresis	]};
    key <AD11> {	[ bracketleft,	braceleft,	udiaeresis,	Udiaeresis	]};
// [...]
```

[Checkout this gist for the full us_umlauts file](https://gist.github.com/raphiz/f48f7062f6ff51cdc34d629bc24063cc)

Finally, I had to set it as default keyboard layout for the X-server - which can be
achieved by editing the file `/etc/X11/xorg.conf.d/00-keyboard.conf` and set the option `XkbLayout`:

```
	 Option "XkbLayout" "us_umlauts"
```

[Checkout this gist for my 00-keyboard.conf file](https://gist.github.com/raphiz/a239e372021a9d218d386b74c843ea1b)

After I logged out and in again, everything worked as expected - at least since I use Xfce.

Before using Xfce  I used Gnome 3 - and Gnome does it's own magic with keyboard layouts.
I could not yet figure out a permanent solution for Gnome - but if you
do, [let me know](/contact/)!
