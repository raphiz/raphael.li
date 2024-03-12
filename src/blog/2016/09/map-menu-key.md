---
title: Change the PrtSc Key to Menu
tags: linux
date: 2016-09-23
---

I got a new Thinkpad recently, and absolute love it.
The only thing I miss is the menu key. I find it very convenient when using graphical applications like the file browser to open the context menu on the selected item.
After a week of moving the mouse around, I decided to replace the PrtSc key (which I never use) with the menu key.

I knew from my previous keyboard experiments that xmodmap would do the job. First, I had to identify the id of the PrtSc key to override it's behaviour. I started `xev` in a Terminal and pressed the key:

```text
KeyPress event, serial 37, synthetic NO, window 0x3c00001,
    root 0xf6, subw 0x0, time 8501035, (32,217), root:(1223,844),
    state 0x0, keycode 107 (keysym 0xff61, Print Screen), same_screen YES,
    XLookupString gives 0 bytes:
    XmbLookupString gives 0 bytes:
    XFilterEvent returns: False

KeyRelease event, serial 37, synthetic NO, window 0x3c00001,
    root 0xf6, subw 0x0, time 8501089, (32,217), root:(1223,844),
    state 0x0, keycode 107 (keysym 0xff61, Print Screen), same_screen YES,
    XLookupString gives 0 bytes:
    XFilterEvent returns: False
```

I first tried to override the keycode (here 107)...

```bash
xmodmap -e "keysym 107 = Menu"
```

... which did not work (It mapped the menu key to the L key?!)

The other identifier is the keysym value - here 0xff61`

```bash
xmodmap -e "keysym 0xff61 = Menu"
```

This command did the job!

All that was left now was to persist it - which is achieved by adding the content of the `-e` switch from the command above into a file called `~/.Xmodmap`.

```text
keysym 0xff61= Menu
```

Logging out and in again - and it the mapping works!
