---
title: "Stop Obsessing Over Micro-Benchmarks - Focus on Real Performance Instead"
tags:
  - java
  - Kotlin
  - Postgres
  - JVM
date: 2024-09-22
---

Recently, I saw a blog post, claiming that [Lists are faster than Sequences](https://chrisbanes.me/posts/use-sequence/). Soon after, the obligatory [contradiction](https://erikvv.github.io/sequence-revenge/) appeared.

Performance discussions like this often miss the point. Instead of focusing on micro-optimizations, developers should prioritize **maintainability and profiling**.

## Performance in the Real World

The Sequence vs. Lists debate is a perfect example of **performance bike-shedding**. Both sides are technically "correct" - they measured numbers for a specific piece of code. But the real question is: **Does the benchmark actually reflect my application's performance concerns?**

For a non-trivial application, neither A nor B is universally right or wrong - it depends on the context.

In most of the performance issues I've encountered in my career, the underlying problem wasn't choosing the "faster" collection type. More often, it came down to **under-fetching or over-fetching**.

For example, the overview page of an application I worked on was "slow." Profiling revealed that **over 3,000 queries** were sent to the database for just a small test data set - exposing both under-fetching (too many small queries) and over-fetching (retrieving unnecessary data). This was a **design issue**, not a List vs. Sequence problem.

So instead of debating micro-benchmarks, here's what actually makes a difference.

## Practical Guidelines for Performance Optimization

I thought this was common knowledge, but apparently, it needs repeating.

### 1. Optimize for Maintainability and Readability - Not for Performance

> **"Premature optimization is the root of all evil."** - Donald Knuth

A good design naturally leads to better performance. Focus on architectural decisions that prevent under- and over-fetching.

### 2. Profile the Application

Profiling under **real-world conditions** provides far more insight than isolated (local) profiling. That said, testing an application in isolation is still better than relying on micro-benchmarks for performance insights.

Tools I've found useful:

- **Java/Kotlin**: [YourKit](https://www.yourkit.com/) (great for both local and production profiling), [IntelliJ Profiler](https://www.jetbrains.com/pages/intellij-idea-profiler/)
- **Databases**: [`EXPLAIN ANALYZE`](https://use-the-index-luke.com/sql/explain-plan/postgresql/getting-an-execution-plan) or production query [statistics](https://www.postgresql.org/docs/9.4/pgstatstatements.html)

Using **real-world data and realistic volumes** is crucial. Databases are a great example: They optimize execution plans based on actual data distribution.

Be open-minded. The bottleneck is often not where you expect.

For example, I once profiled an application suffering from random reboots. We initially suspected slow serialization. There was even a home-grown serialization implementation that was supposedly "faster." But after measuring and observing the application, it turned out that an expensive serialization operation was accidentally executed for each subscriber instead of once globally. This was hidden deep inside the custom serialization code - which was a premature optimization in the first place.

### 3. Experiment

Try different approaches. Depending on your use case, switching from Lists to Sequences _might_ show some difference - but a small improvement doesn't mean it's worth changing your approach. Focus on optimizations with a significant impact.

### 4. Optimize Selectively

Maintainability and readability are more important than performance. Keep that in mind before applying any optimization.

### 5. Ideally: Measure Continuously

Performance isn't static. What's fast today may not be in two years. If performance is critical, verify it continuously.

## Conclusion

Let's stop debating micro-benchmarks - they rarely matter in real-world applications.

Instead, let's focus on mastering **profiler tools and techniques** - and sharing our experiences and insights with them.
