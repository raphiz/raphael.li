---
layout: post
title: Remeber position in VLC
tags: linux
---
Sometimes I get distracted when watching movies, series, video tutorials etc. or there is just not enough time to finish the video.

Never can I remeber the position where I stopped (eg. 25:45) and taking notes is not exactly comfortable. VLC has no built-in function to remeber the position - but luckily there is an plugin for this. It's called *VLC srpos plugin* and can be downloaded on [Sourceforge](http://sourceforge.net/projects/vlcsrposplugin/?source=typ_redirect).

After downloading, all that's left to do is extract, compile and install it. This is pretty much straight forward for Linux users:

```bash
$ tar -xf libsrpos_plugin-0.5.tar.gz
$ cd libsrpos_plugin-0.5/
$ ./configure
$ make
$ sudo make install
```

Restart VLC and go into the preferences (Check `Show all preferences`). Check the new checkbox in the submenu `Interface/Control interface` called `save/restore position of the last played file`.

{% image resources/vlc_restore/screenshot.png %}

<small>(Screenshot taken from vlcsrposplugin.sourceforge.net)</small>

For more information, checkout the the [VLC srpos plugin Website](http://vlcsrposplugin.sourceforge.net/)

Happy watching!
