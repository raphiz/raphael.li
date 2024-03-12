---
title: Java MessageFormat considered harmful
tags:
  - java
  - JVM
date: 2024-03-12
---

If you've worked with Java for a while, you're likely familiar with the `MessageFormat` class. At first glance, it appears to be a straightforward tool for formatting, internationalization and localization, but the devil is in the details.

## MessageFormat Basics

The MessageFormat class allows you to define a template string with (numeric) placeholders for variables, which are then substituted with actual values at runtime. Here's a basic example:

```java
String pattern = "Hello, {0}! You are visitor number {1}.";
MessageFormat formatter = new MessageFormat(pattern, Locale.FRANCE);
Object[] arguments = {"Alice", 10000};
String formatted = formatter.format(arguments);
System.out.println(formatted);
// Output: Hello, Alice! You are visitor number 10 000.
```

Note that the output of the visitor number depends on the provided locale, in our example `Locale.FRANCE`

## The Pitfalls of Single Quotes

Consider the following example:

```java
String pattern = "Don't touch that, {0}";
MessageFormat formatter = new MessageFormat(pattern, Locale.FRANCE);
Object[] arguments = {"Alice"};
String formatted = formatter.format(arguments);
System.out.println(formatted);
```

You would expect it to print `Don't touch that, Alice`, but it actually prints `Dont touch that, {0}`. The reason is, that single quotes are used as escaping Characters within `MessageFormat` patterns.

The [Documentation](https://docs.oracle.com/javase/8/docs/api/java/text/MessageFormat.html) even warns us about this - but who reads the docs anyways...

> The rules for using quotes within message format patterns unfortunately have shown to be somewhat confusing. In particular, it isn't always obvious to localizers whether single quotes need to be doubled or not. Make sure to inform localizers about the rules, and tell them (for example, by using comments in resource bundle source files) which strings will be processed by MessageFormat. Note that localizers may need to use single quotes in translated strings where the original version doesn't have them.

Single quotes are commonly used characters in various languages, such as French and Italian and even English, making it a terrible choice for an escaping character.
The worst of this, is that's relatively easy to overlook problems, for example when the locale you are developing in does not use a lot of these single quotes.

To fix our example, we have to use `''` instead of `'`. Have fun explaining that to your localizers...

```java
String pattern = "Don''t touch that, {0}";
MessageFormat formatter = new MessageFormat(pattern, Locale.FRANCE);
Object[] arguments = {"Alice"};
String formatted = formatter.format(arguments);
System.out.println(formatted);
```

## Exploring Alternatives

I personally find the `MessageFormat` to be an insufficient solution for localization anyways.

Depending on you use case, I recommend a simple string substitution or looking for a fully fledget i18n solution.

### Simple String Substitution

You may reach out for Apache Commons Text's `StringSubstitutor`. This class provides a straightforward way to handle string substitution without the hidden complexities of MessageFormat.

Here's an example:

```java
import org.apache.commons.text.StringSubstitutor;
import java.text.NumberFormat
import java.util.Locale

Map<String, String> valuesMap = new HashMap<>();
valuesMap.put("name", "Alice");
valuesMap.put("number", NumberFormat.getIntegerInstance(Locale.FRANCE).format(10000));

String pattern = "Hello, ${name}! You are visitor number ${number}.";
StringSubstitutor substitutor = new StringSubstitutor(valuesMap);
System.out.println(substitutor.replace(pattern));

// Output: Hello, Alice! You are visitor number 10 000.
```

This approach not only eliminates the need to escape single quotes, it also uses named placeholders, which helps localizers understanding what these are standing for in the first place.

### fully fledget i18n solution

[icu4j](https://unicode-org.github.io/icu-docs/) looks very promising, but unfortunately I do not have any experience with it (yet).

icu4j not only seem to address the Single Quotes pitfalls but has also support for propper pluralization etc.

## Conclusion

In summary, Java's `MessageFormat` class, though initially appealing for localization, poses challenges due to its handling of single quotes, potentially causing errors in internationalization.
Consider simpler alternatives like Apache Commons Text's `StringSubstitutor` or comprehensive i18n solutions such as icu4j for more streamlined and intuitive localization efforts.
