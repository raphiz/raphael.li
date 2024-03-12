---
title: UTF-8 Normalization
tags:
  - Kotlin
  - Postgres
  - JVM
date: 2022-09-21
---

In Unicode, the same character can be represented using different sequences of code points.

> For example, the code point U+006E (the Latin lowercase "n") followed by U+0303 (the combining tilde "◌̃") is defined by Unicode to be canonically equivalent to the single code point U+00F1 (the lowercase letter "ñ" of the Spanish alphabet). - [Wikipedia **Unicode equivalence**](https://en.wikipedia.org/wiki/Unicode_equivalence)

This is a problem when you have one representation in your DB and query the same string using a different one. I never had this issue before, but ran into it recently when reading file names from a macOS file system. This seems to be a legacy issue.

So what can we do? We can use normalization forms to ensure the character is always represented in the same way. There are multiple normal forms, but [`NFC`](https://en.wikipedia.org/wiki/Unicode_equivalence#Combining_and_precomposed_characters) is the one you probably want.

The best place to do this normalization is where you perform other validation, eg. in your Web API Controllers.

```kotlin

import java.text.Normalizer
// ...

@PostMapping
fun postFile(fileName: String){
  val normalized = Normalizer.normalize(fileName, Normalizer.Form.NFC)
  // ...
}
```

If you have the mess already and different forms are mixed in your database, you can normalize it (in Postgres) using the [`normalize`](https://www.postgresql.org/docs/current/functions-string.html#id-1.5.8.10.5.2.2.7.1.1.2) function:

```sql
update files
set filename = normalize(filename);
```

See also:

- [Wikipedia - Unicode equivalence](https://en.wikipedia.org/wiki/Unicode_equivalence)
- [JDK Documentation - Normalizing Text](https://docs.oracle.com/javase/tutorial/i18n/text/normalizerapi.html)
- [unicode.org - Normalization FAQ](https://unicode.org/faq/normalization.html)
- [Blogpost on 2ndquadrant.com - Unicode normalization in PostgreSQL 13](https://www.2ndquadrant.com/en/blog/unicode-normalization-in-postgresql-13/)
-
