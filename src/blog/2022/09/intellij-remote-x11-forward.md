---
title: IntellIJ remote development with good old X11 forwarding
tags:
  - linux
date: 2022-09-21
---

I played around with IntelliJs [Remote Development](https://www.jetbrains.com/remote-development/) functionality recently.

It works mostly, but there are a few bugs or inconsistencies between a local installation and the Remote Access that killed my productivity.

So I switched back to the good old X11 Forwarding🙂

The Setup was quite simple:

## Enable X11 Forwarding on the Remote Host

```Plain
...
X11Forwarding yes
```

## Enable X11 Forwarding on the Guest Host

```Plain
Host my-remote-host
    HostName my-remote-host
    ForwardX11 yes
    ForwardX11Trusted yes
```

## Launch IntelliJ

Now, I can simply launch my remote IDE as follows

```Bash
ssh user@my-remote-host "intellij-idea-ultimate-edition ~/workspace/ &>/dev/null"
```

So far It seems much better than the built-in solution from IntelliJ - but let’s see how It plays out over a few weeks.

## Alternativen

This obviously only works for the (deprecated) X11 Window Server - For Wayland, [Waypipe](https://gitlab.freedesktop.org/mstoeckl/waypipe/) seems like a good option (haven't tried it out yet).
