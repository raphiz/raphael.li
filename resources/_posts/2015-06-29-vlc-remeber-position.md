---
layout: post
title: Remeber position in VLC
tags: linux
---
Sometimes I get distracted when watching films, series, video tutorials etc. or there is just not enough time to finish the video.

Never can I remember the position where I stopped (e.g. 25:45) and taking notes is not exactly comfortable. VLC has no built-in function to remember the position - but luckily there is a plug-in for this. It's called *VLC srpos plug-in* and can be downloaded on [Sourceforge](http://sourceforge.net/projects/vlcsrposplugin/?source=typ_redirect).

After downloading, all that's left to do is extract, compile and install it. This is pretty much straight forward for Linux users:

```bash
$ tar -xf libsrpos_plugin-0.5.tar.gz
$ cd libsrpos_plugin-0.5/
$ ./configure
$ make
$ sudo make install
```

Restart VLC and go into the preferences (Check `Show all preferences`). Check the new check box in the sub menu `Interface/Control interface` called `save/restore position of the last played file`.

{% image resources/vlc_restore/screenshot.png %}

<small>(Screenshot taken from vlcsrposplugin.sourceforge.net)</small>

For more information, checkout the [VLC srpos plug-in Website](http://vlcsrposplugin.sourceforge.net/)

Happy watching!
