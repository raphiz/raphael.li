---
title: Auto-update JDK version with Renovate
tags:
  - JVM
  - Kotlin
  - Gradle
date: 2024-06-11
---

I like [renovate](https://docs.renovatebot.com/) a lot and use it to keep all my dependencies up to date.

What does not work out of the box in my Gradle projects is updating the JDK (or more precisely, the [JVM toolchain](https://docs.gradle.org/current/userguide/toolchains.html)).

Here is a simple example of such a Gradle projects's `build.gradle.kts` file:

```kotlin
import org.jetbrains.kotlin.gradle.dsl.KotlinVersion

plugins {
    kotlin("jvm") version "2.0.0"
    application
}

// ...

kotlin {
    jvmToolchain(21) // <-- Keep me up-to-date!
    compilerOptions {
        freeCompilerArgs.set(listOf("-Xjsr305=strict"))
    }
}

```

To update the `jvmToolchain` here, we can use a `customManager` from renovate as follows:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],

  "customManagers": [
    {
      "customType": "regex",
      "description": "Update Java Version",

      // match all files called `build.gradle.kts`.
      "fileMatch": ["(^|.*/)build.gradle.kts$"],

      // Find the relevant location in the file: jvmToolchain(...)
      "matchStrings": ["jvmToolchain\\((?<currentValue>.*)\\)"],

      // Figure out the "latest GA version" from the openjdk/jdk repo tags
      "datasourceTemplate": "github-tags",
      "depNameTemplate": "openjdk/jdk",
      "extractVersionTemplate": "^jdk-(?<version>.+?)-ga$",

      "versioningTemplate": "loose"
    }
  ]
}
```

With this configuration, renovate will create a PR when a new major JDK version is released.

Happy updating 🚀
