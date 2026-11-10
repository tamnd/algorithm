---
tag: T7790D
kind: model
slug: cash-register-model
name: Cash register model
aliases:
- insertion-only model
- increment-only model
- insertion-only streams
area: online-and-streaming/streaming-sketches
level: intro
summary: Stream updates only increase counts of items.
prereqs: [streaming-model, frequency-vector]
see_also: [turnstile-model, misra-gries-summary, reservoir-sampling, kmv-sketch, hyperloglog, greenwald-khanna-summary, morris-counter, mergeable-summaries]
sources:
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: Chapter Data Streaming, Formal Aspects, section Data Stream Models (the cash register model, in which each update is an increment)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1, Introduction (insertion-only and turnstile streams)
  - paper: doi:10.1145/2213556.2213562
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, PODS 2012
    locator: pp. 23 to 34 (summaries for insertion-only data that also merge)
---

The cash register model is the update model of the [streaming model](/streaming-model/) in which each update only adds to the count of an item. The stream is a sequence of updates $(i_j, \Delta_j)$ with $i_j \in [n]$ and $\Delta_j > 0$, and the [frequency vector](/frequency-vector/) $f$ only grows. In the most common case $\Delta_j = 1$, and the stream is a plain sequence of $m$ items $a_1, \ldots, a_m$. The name, from Muthukrishnan (2005), comes from a till that only adds sales. It is also called the insertion-only model. On this page $m$ is the number of updates and $n$ is the universe size.

## The machine

The machine is the streaming machine: $s$ bits of memory, one pass, an update step per item and a query. What the model fixes is the form of the input.

- Each update is a pair $(i, \Delta)$ with $i \in [n]$ and $\Delta$ a positive integer of $O(\log m)$ bits, or just an item $i$, which means $\Delta = 1$.
- After $j$ updates, $f_i$ is the sum of the $\Delta$ of the updates to $i$ so far. So $f \ge 0$, and each $f_i$ is a nondecreasing function of $j$.
- With unit updates, $\|f\|_1 = m$, and the set of items seen so far is the support $\{i : f_i > 0\}$.

Muthukrishnan also gives the time series model, where the $j$-th update is the value of $f_j$ itself. It is a special case of the cash register model in which each item appears once.

## What it counts

The costs are those of the streaming model: the space in bits, the update time, the query time, the number of passes, and the error $\varepsilon$ with failure probability $\delta$. Two quantities are free here. The length $m$ of a unit stream, or the total weight $\|f\|_1$, fits in an exact counter of $O(\log(m \max \Delta))$ bits, so an additive error of $\varepsilon\|f\|_1$ has a known scale. And each statistic that is monotone in $f$, such as the number of distinct items or the largest count, only grows, so a summary never has to undo an update.

## Relation to other models

- **Inside the turnstile model.** Each cash register stream is a [strict turnstile](/turnstile-model/) stream, and each strict turnstile stream is a general turnstile stream. So each turnstile algorithm also works here, with the same bounds. The converse fails: many cash register algorithms keep items or hash values that a deletion would make wrong.
- **Lower bounds go the other way.** A lower bound in the cash register model is also a lower bound in the turnstile models. Most of the classic lower bounds, such as the $\Omega(n)$ bits for an exact count of distinct items, are already proved for insertion-only streams.
- **Merges.** For insertion-only data, the union of two data sets is the concatenation of two streams. So a [mergeable summary](/mergeable-summaries/) of each part gives a summary of the whole, and many insertion-only summaries are mergeable.
- **Sliding windows.** In the [sliding window model](/sliding-window-model/) the stream is insertion-only, but old items leave the window. An expiry is a deletion that the algorithm can predict, which makes the model lie between the cash register and the turnstile models.

## Known results in the model

**Proved here: summaries of the set of seen items.** Let $g$ be a function of the support $T_j = \{i : f_i > 0\}$ after $j$ updates. In the cash register model $T_{j} = T_{j-1} \cup \{i_j\}$. So if a summary $S(T)$ has an update map $U$ with $S(T \cup \{i\}) = U(S(T), i)$, then the algorithm "$S \leftarrow U(S, i_j)$ for each update" keeps $S(T_j)$ for each $j$, and repeats of an item do not change $S$ when $U(S(T), i) = S(T)$ for $i \in T$. The bitmap of [Flajolet and Martin](/flajolet-martin-algorithm/), the registers of [HyperLogLog](/hyperloglog/) and the $k$ smallest hash values of a [KMV sketch](/kmv-sketch/) are summaries of this kind, with $U$ an OR, a maximum or a merge of sorted lists. In a turnstile stream the support can lose an item, $T_j = T_{j-1} \setminus \{i\}$, and these maps have no inverse: after the item with the smallest hash value is deleted, the KMV sketch does not know the $(k+1)$-th smallest value. $\square$

The algorithms in the table below use the insertion-only form of the stream: they fail, or need another method, under deletions. The bounds are cited here and proved on the linked pages.

| problem | algorithm | space | guarantee |
|---|---|---|---|
| count the items | [Morris counter](/morris-counter/) | $O(\log\log m)$ bits for constant $\varepsilon, \delta$ | randomized, relative |
| distinct items | [HyperLogLog](/hyperloglog/), [KMV](/kmv-sketch/) | $O(\varepsilon^{-2})$ registers or hash values | randomized, relative |
| heavy hitters | [Misra-Gries](/misra-gries-summary/), [Space-Saving](/space-saving/) | $O(1/\varepsilon)$ counters | deterministic, additive $\varepsilon m$ |
| quantiles | [Greenwald-Khanna](/greenwald-khanna-summary/) | $O(\varepsilon^{-1}\log(\varepsilon m))$ words | deterministic, rank error $\varepsilon m$ |
| quantiles | [KLL](/kll-sketch/) | $O(\varepsilon^{-1}\log\log(1/\delta))$ words | randomized, rank error $\varepsilon m$ |
| uniform sample of $k$ items | [reservoir sampling](/reservoir-sampling/) | $k$ items | exact distribution |
| majority element | [Boyer-Moore](/boyer-moore-majority/) | 2 words | exact, if a majority exists |

## References
