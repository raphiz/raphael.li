---
title: "Turning Jackson into a Kotlin-Friendly JSON DSL"
tags:
  - Kotlin
  - java
  - JVM
date: 2025-03-08
---

When writing tests, I often need to craft JSON payloads manually - for example, to build API requests. While Jackson is a powerful library for working with JSON in Java and Kotlin, its API can be a bit verbose, making manual JSON construction cumbersome.

Fortunately, Kotlin's extension functions allow us to transform Jackson into a more expressive, Kotlin-friendly JSON builder. In this post, I'll show how we can make JSON construction cleaner, more readable, and safer - without introducing additional dependencies.

## Why Not Just Use String Interpolation?

A common way to construct JSON is through string interpolation, as shown below:

```kotlin
val value = "value with a quote \" "
val result = """
{
  "string" : "$value",
  "object" : {
    "number" : 42
  },
  "array" : [ ],
  "number" : 42,
  "emptyObject" : { },
  "emptyArray" : [ ]
}
""".trimIndent()
.also(::println)
```

However, this approach has significant drawbacks. Since the JSON is manually assembled as a raw string, it is not properly sanitized, which can lead to errors, especially when handling quotes.

## A Better Approach: Using Jackson

A safer alternative is to construct JSON using Jackson. While the API is flexible, it can be a bit tricky to use, and there are multiple ways to achieve the same result. We'll use the `JsonNodeFactory` in the following example.

```kotlin
import com.fasterxml.jackson.databind.node.JsonNodeFactory

fun main() {
    val root = JsonNodeFactory.instance.objectNode()
    root.put("string", "value")

    val anObject = root.putObject("object")
    anObject.put("number", 42)

    val numbers = root.putArray("numbers")
    numbers.add(4)
    numbers.add(8)
    numbers.add(15)

    val strings = root.putArray("strings")
    strings.add("a")
    strings.add("b")

    root.putObject("emptyObject")
    root.putArray("emptyArray")

    root.toPrettyString()
        .also(::println)
}
```

While you can probably figure out what's happening here, it's not obvious, especially for nested constructs. We also have to name intermediate objects (such as `anObject`, `numbers`, etc.), which gets messy for more complicated payloads. But luckily, Kotlin has a nice trick up its sleeve to make things more readable.

## `apply` to the Rescue

To get rid of the intermediate objects and to reflect the nested structure, we can leverage Kotlin's [`apply`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/apply.html) function:

```kotlin
import com.fasterxml.jackson.databind.node.JsonNodeFactory

fun main() {
    JsonNodeFactory.instance.objectNode().apply {
        put("string", "value")
        putObject("object").apply {
            put("number", 42)
        }
        putArray("numbers").apply {
            add(4)
            add(8)
            add(15)
        }
        putArray("strings").apply {
            add("a")
            add("b")
        }
        putObject("emptyObject")
        putArray("emptyArray")
    }
    .toPrettyString()
    .also(::println)
}
```

## Improving Readability Further with Extension Functions

The frequent calls to `apply` and `JsonNodeFactory` are still quite noisy. We can clean this up by introducing a few simple extension functions:

```kotlin
import com.fasterxml.jackson.databind.node.ArrayNode
import com.fasterxml.jackson.databind.node.JsonNodeFactory
import com.fasterxml.jackson.databind.node.ObjectNode

fun main() {
    obj {
        put("string", "value")
        putObject("object") {
            put("number", 42)
        }
        putArray("numbers") {
            add(4)
            add(8)
            add(15)
        }
        putArray("strings") {
            add("a")
            add("b")
        }
        putObject("emptyObject")
        putArray("emptyArray")
    }
    .toPrettyString()
    .also(::println)
}

fun obj(block: ObjectNode.() -> Unit): ObjectNode =
    JsonNodeFactory.instance.objectNode().apply(block)

fun ObjectNode.putObject(propertyName: String, block: ObjectNode.() -> Unit): ObjectNode =
    putObject(propertyName).apply(block)

fun ObjectNode.putArray(propertyName: String, block: ArrayNode.() -> Unit): ArrayNode =
    putArray(propertyName).apply(block)
```

With these few simple extension functions, our JSON-building code is now much cleaner and easier to read.

## Further Simplifications for Specific Use Cases

The extension functions shown above remove most of the unnecessary noise. Depending on the use case, we can streamline it further. Let's say we have lots of arrays - so let's optimize for that. Again, with just a few extension functions:

```kotlin
import com.fasterxml.jackson.databind.node.ArrayNode
import com.fasterxml.jackson.databind.node.JsonNodeFactory
import com.fasterxml.jackson.databind.node.ObjectNode
import java.math.BigDecimal

fun main() {
    obj {
        put("string", "value")
        putObject("object") {
            put("number", 42)
        }
        putArray("numbers", listOf(4, 8, 15))
        putArray("strings", listOf("a", "b", "c"))
        putObject("emptyObject")
        putArray("emptyArray")
    }
    .toPrettyString()
    .also(::println)
}

fun obj(block: ObjectNode.() -> Unit): ObjectNode =
    JsonNodeFactory.instance.objectNode().apply(block)

fun ObjectNode.putObject(propertyName: String, block: ObjectNode.() -> Unit): ObjectNode =
    putObject(propertyName).apply(block)

fun ObjectNode.putArray(propertyName: String, block: ArrayNode.() -> Unit): ArrayNode =
    putArray(propertyName).apply(block)

@JvmName("putArrayOfStringCollection")
fun ObjectNode.putArray(propertyName: String, elements: Collection<String>): ArrayNode =
    putArray(propertyName).also { array ->
        elements.forEach { element ->
            array.add(element)
        }
    }

@JvmName("putArrayOfNumberCollection")
fun ObjectNode.putArray(propertyName: String, elements: Collection<Number>): ArrayNode =
    putArray(propertyName).addAll(
        elements.map { JsonNodeFactory.instance.numberNode(it as? BigDecimal ?: BigDecimal(it.toString())) }
    )
```

There is no right or wrong here. I'll try to design these in my projects to feel as natural as possible for the specific use case. And of course, it's a matter of taste too.

## Alternative Solutions

There are also existing libraries, such as [Koson](https://github.com/lectra-tech/koson), that provide DSLs for constructing JSON. I find these extension functions to be a simple and effective solution when using Jackson already in a project - without adding an extra dependency.

## Summary

- This approach is **safer** than using string interpolation.
- The resulting code is **more readable** and **more flexible** compared to raw Jackson API usage.
- It **avoids unnecessary dependencies**, making it a lightweight solution.
