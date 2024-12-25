---
title: Remember position in VLC
tags: linux
date: 2015-06-29
---

Sometimes I get distracted when watching films, series, video tutorials etc. or there is just not enough time to finish the video.

Never can I remember the position where I stopped (was it 25:45 or 45:25?) and taking notes is not exactly comfortable. VLC has no built-in function to remember the position - but luckily there is a plug-in for this. It's called _VLC srpos plug-in_ and can be downloaded on [Sourceforge](https://sourceforge.net/projects/vlcsrposplugin/).

After downloading, all that's left to do is to extract, compile and install it. This is pretty much straight forward for Linux users:

```bash
tar -xf libsrpos_plugin-0.5.tar.gz
cd libsrpos_plugin-0.5/
./configure
make
sudo make install
```

Restart VLC and open the preferences dialog (Check `Show all preferences`). Select the checkbox in the submenu `Interface/Control interface` called `save/restore position of the last played file`.

{% image "./screenshot.png", "Screenshot of the configuration screen" %}

(Screenshot taken from vlcsrposplugin.sourceforge.net)

For more information, checkout the [VLC srpos plug-in Website](http://vlcsrposplugin.sourceforge.net/)

Happy watching!
