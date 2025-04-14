---
title: Handling Vulnerable Transitive Dependencies in Gradle
tags:
  - java
  - Kotlin
  - JVM
date: 2025-04-14
---

When working on projects that use Gradle, I frequently encounter a well-intentioned but ultimately harmful dependency management pattern.
It's a mistake that often comes from a good place, security awareness, and yet it ends up introducing more problems than it solves.

Let's break it down with an example

## The Good Intentions

Security scanners like [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/), [Snyk](https://snyk.io/), or [GitHub's Dependabot](https://docs.github.com/en/code-security) are helpful tools.
They'll notify us about known vulnerabilities in (transitive) dependencies of our code base.

Let's say such a tool warns us about a vulnerability in one of the libraries our project uses.
Dependency `example-library` pulls in `log4j` version `2.14.1`, which has known vulnerabilities (among others, the famous [Log4Shell](https://en.wikipedia.org/wiki/Log4Shell)).
We can verify that by running `gradle dependencies`

```text
...
+--- com.example:example-library:1.42.0
|    +--- org.apache.logging.log4j:log4j-core:2.14.1
...
```

Sadly, there is no newer version of `example-library` available (yet) that updates this transitive dependency.

## The (wrong) fix: Adding a Direct Dependency

What often follows is this:

```kotlin
dependencies {
    // our existing, direct dependency
    implementation("com.example:example-library:1.42.0")

    // not a direct dependency, but added to upgrade the transitive dependency of example-library
    implementation("org.apache.logging.log4j:log4j-core:2.15.0")
}
```

So instead of letting `example-library` control what version of `log4j` it uses, we pin it ourselves.

To see if it works, let's run `gradle dependencies` again:

```text
...
+--- com.example:example-library:1.42.0
|    +--- org.apache.logging.log4j:log4j-core:2.14.1 -> 2.15.0
+--- org.apache.logging.log4j:log4j-core:2.15.0 (*)
...

(*) - Indicates repeated occurrences of a transitive dependency subtree. Gradle expands transitive dependency subtrees only once per project; repeat occurrences only display the root of the subtree, followed by this annotation.
```

And it is working: The newer version of `log4j` is being used and the scanner stops complaining.

But note what happens if we remove `example-library` from our dependencies block:

```text
...
+--- org.apache.logging.log4j:log4j-core:2.15.0
...

```

## The Cost of That Direct Dependency

Let's unpack the implications of what we did:

- **Unintentional Ownership**: By adding a direct dependency on `log4j`, we've taken ownership of a library we don't actually use ourselves.
  That means we're now responsible for keeping it updated and ensuring it is compatible with what `example-library` expects.
  If `example-library` removes or changes its `log4j` version later, we may accidentally keep dragging it along or introduce unnecessary version conflicts.
- **The wrong Message**: This also sends the wrong message - to both Gradle's resolution mechanism and future developers reading our build file.
  Instead of saying "make sure to use a safe version of `log4j` if it's on the classpath", we're saying "we depend directly on `log4j` version `2.15.0`".

Luckily, there's a better way.

## Use Dependency Constraints Instead

We don't want to take over transitive dependencies, but instead formulate [**dependency constraints**](https://docs.gradle.org/current/userguide/dependency_constraints.html).

And Gradle has a dedicated DSL for that:

```kotlin
dependencies {
    // Note: The `constraints` block lives inside the `dependencies` block
    constraints {
        implementation("org.apache.logging.log4j:log4j-core") {
            because("earlier versions are vulnerable to the Log4Shell vulnerability")
            version {
                require("2.15.0")
            }
        }
    }
}
```

This [DSL is quite flexible](https://docs.gradle.org/current/userguide/dependency_versions.html#sec:rich-version-constraints).
We used `require` here but depending on your use case, `reject` or `strictly` are what you want.

Let's run `gradle dependencies` again:

```text
...
+--- com.example:example-library:1.42.0
|    +--- org.apache.logging.log4j:log4j-core:2.14.1 -> 2.15.0
+--- org.apache.logging.log4j:log4j-core:2.15.0 (c)
...

(c) - A dependency constraint, not a dependency. The dependency affected by the constraint occurs elsewhere in the tree.
```

The effect is the same, but if we remove `example-library` from our `dependencies` block, `log4j` is gone.

I think the biggest benefit, apart from properly naming that it's a constraint, is that we can forget about it!
Once added, we don't have to think about it again.

## Bonus: Sharing Constraints via Convention Plugins and Platforms

In smaller projects, such constraints can be shared via [convention plugin](https://docs.gradle.org/current/samples/sample_convention_plugins.html).

For larger or company-wide setups, we can define constraints like this in shared [platform](https://docs.gradle.org/current/userguide/platforms.html) modules.
That way, our policy is centralized and explicit.

Note that we can't express such constraints with [version catalogs](https://docs.gradle.org/current/userguide/version_catalogs.html).
See [Benedikt Ritter's excellent write-up](https://britter.dev/blog/2025/01/24/version-catalogs-vs-platforms/) for further details

## In Summary

Next time a security scanner tells you a transitive dependency is vulnerable, use Gradle's `constraints` DSL to express your intent clearly.
