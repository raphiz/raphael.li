---
title: "When Turbo Won't Turbo: Fixing Unexpected Full Page Reloads"
tags:
  - web
  - hotwired
date: 2024-09-22
---

I wanted to incorporate my beloved [Hotwired Turbo](https://turbo.hotwired.dev/) into one of my projects. After all, it's just a matter of adding an import, right?

```javascript
import * as Turbo from "https://unpkg.com/@hotwired/turbo@8.0.10/dist/turbo.es2017-esm.js";
```

I did just that, but navigating between pages still resulted in a full page reload, even though the library was successfully fetched from the CDN. Logging `window.Turbo` confirmed that the library was present. Even more puzzling, I was able to navigate using `Turbo.visit(...)`, but it still caused a full page reload.

It turns out Turbo Drive is working as expected. The problem was on the server side. Here's the (simplified) [http4k](https://www.http4k.org/) code - can you spot the error?

```kotlin
routes(
    "/" bind {
        val template = Path.of("index.html").readText()
        Response(Status.OK).body(html)
    },
).asServer(SunHttp(8080)).start()
```

I had simply forgotten to add the `Content-Type` header 🤦.

```kotlin
routes(
    "/" bind {
        val template = Path.of("index.html").readText()
        Response(Status.OK)
            .header("Content-Type", "text/html")
            .body(html)
    },
).asServer(SunHttp(8080)).start()
```

Well, at least I've learned something today.
