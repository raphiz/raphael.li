---
title: "Fixing: `Error opening file '/nix/store/....drv'`"
tags:
  - java
  - JVM
date: 2024-06-05
---

When I tried to deploy one of my NixOS systems today, I got the following error:

```bash
$nix build .#nixosConfigurations.my-host.config.system.build.toplevel
error:
       … while calling the 'head' builtin

         at /nix/store/lwlxkldi1f35lj2ghlxgc73fyfa181i8-source/lib/attrsets.nix:1575:11:

         1574|         || pred here (elemAt values 1) (head values) then
         1575|           head values
             |           ^
         1576|         else

       … while evaluating the attribute 'value'

         at /nix/store/lwlxkldi1f35lj2ghlxgc73fyfa181i8-source/lib/modules.nix:809:9:

          808|     in warnDeprecation opt //
          809|       { value = builtins.addErrorContext "while evaluating the option `${showOption loc}':" value;
             |         ^
          810|         inherit (res.defsFinal') highestPrio;

       (stack trace truncated; use '--show-trace' to show the full trace)

       error: opening file '/nix/store/5c8lwrmlc7ckk4j5dd1ympiz3w8syjx9-busybox.drv': No such file or directory
```

This is confusing - it seems like this busybox derivation should be in my Nix store, but it's not.
I'm not exactly sure what the cause is, but probably the GC running in the background at more or less the same time.

I checked the Nix database for consistency, and voilla:

```bash
$ nix-store --verify
reading the Nix store...
checking path existence...
path '/nix/store/5c8lwrmlc7ckk4j5dd1ympiz3w8syjx9-busybox.drv' disappeared, but it still has valid referrers!
path '/nix/store/q61l6anrvv4qjw2mjv1lby7z2ij3px6s-set-correct-program-name-for-sleep.patch' disappeared, but it still has valid referrers!
path '/nix/store/sg9qz439fx55m7y3z76lja6v6gg38a5p-extension-dir.patch' disappeared, but it still has valid referrers!
```

It seems that some paths have disappeared from my Nix store. So let's fix that:

```bash
sudo nix-store --repair-path /nix/store/5c8lwrmlc7ckk4j5dd1ympiz3w8syjx9-busybox.drv
sudo nix-store --repair-path /nix/store/q61l6anrvv4qjw2mjv1lby7z2ij3px6s-set-correct-program-name-for-sleep.patch
sudo nix-store --repair-path /nix/store/sg9qz439fx55m7y3z76lja6v6gg38a5p-extension-dir.patch
```

Note that the command will fail with the unhelpful message `error: operation 'repairPath' is not supported by store 'daemon'' if you are missing some permissions - run the command as root instead.

And that solved the problem🤞
