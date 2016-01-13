---
layout: project
title: Lombok restricted access
type: experiment
github: https://github.com/raphiz/lombok_restricted_access
teaser: Custom Access Modifiers with Lombok
initiation: 2014
status: inactive
---

The idea is to build something like [Kohsuke Kawaguchi's  Custom Access Modifier](http://www.kohsuke.org/access-modifier/)
as a custom [Lombok](http://projectlombok.org/) handler. When using Lombok, no Maven-Plugins or any other build magic is required - just
adding the dependencies and it works.

You annotate the methods that shall not be called outside of your Framework with the RestrictedAccess annotation.
At compile time, Lombok's magic injects a check if the caller of the method/constructor is in the allowed package.
If not, an RuntimeException is thrown.

```java
package my.private.api.internal;
   public class PrivateAPI {
    @RestrictedAccess("my.private.api")
    public PrivateAPI() {
        // DO private stuff
    }
}
```

```java
package third.party.app;
...
   new PrivateApi().doStuff()
...
}
```

A working example can be found in the sub project *example_usage*

**This is only a proof of concept. Production usage is not recommended!**
