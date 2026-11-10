---
tag: 9WYFEF
kind: problem
slug: frequent-items-problem
name: Frequent items problem
aliases:
- heavy hitters problem
- top-k frequent items
- epsilon-approximate frequent items
- iceberg queries
area: online-and-streaming/streaming-sketches
level: core
summary: Report all items whose count exceeds a fraction of the stream length, with approximate counts.
prereqs: [streaming-model, frequency-vector, majority-element-problem]
see_also: [misra-gries-summary, space-saving, lossy-counting, count-min-sketch, count-sketch, frequency-estimation, sliding-window-heavy-hitters, index-problem-lower-bound]
sources:
  - paper: "Gurmeet Singh Manku and Rajeev Motwani, Approximate frequency counts over data streams, Proceedings of the 28th International Conference on Very Large Data Bases (VLDB), 2002, pages 346 to 357"
    locator: the definition of the problem with support s and error ε, and the guarantees of an ε-deficient synopsis
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (Misra-Gries, SpaceSaving, Count-Min and Count Sketch for heavy hitters)
  - url: https://web.stanford.edu/class/cs168/l/l2.pdf
    title: Tim Roughgarden and Gregory Valiant, CS168 The Modern Algorithmic Toolbox, Lecture 2, Approximate heavy hitters and the count-min sketch, Stanford University
    locator: Section 2, the heavy hitters problem and its ε-approximate version, and the one-pass lower bound for the exact version
  - paper: doi:10.1145/1562764.1562789
    title: Graham Cormode and Marios Hadjieleftheriou, Finding the frequent items in streams of data, Communications of the ACM 52(10), 2009
    locator: the survey of counter-based and sketch-based algorithms and their experimental comparison
---

The frequent items problem, also called the heavy hitters problem, asks for the items of a stream whose count is more than a fraction $\phi$ of the stream length $m$. One pass cannot solve it exactly in small memory, so the standard version allows an error $\varepsilon m$: report every item with count more than $\phi m$, and no item with count less than $(\phi - \varepsilon) m$. Deterministic counter-based summaries such as [Misra-Gries](/misra-gries-summary/) and [Space-Saving](/space-saving/) solve it with $O(1/\varepsilon)$ words on insertion-only streams. Randomized linear sketches such as the [count-min sketch](/count-min-sketch/) and the [count sketch](/count-sketch/) solve it also when items are deleted.

## In plain words

A web server sees millions of requests, and you want the pages that get more than 1 percent of them. You cannot keep a tally for every page. The good news is that at most 100 pages can be above 1 percent, so a short list can hold all of them.

The bad news is that you cannot find the exact list in one pass with little memory. So you accept a small blur: a page with 1 percent must be on the list, a page with less than 0.9 percent must not be, and a page in between may go either way. Several simple methods give this list with a few hundred tallies.

## Definition

The input is a stream $\sigma = a_1, \ldots, a_m$ of items from the universe $[n] = \{1, \ldots, n\}$, with [frequency vector](/frequency-vector/) $f$, so $f_x$ is the number of times $x$ occurs and $\sum_x f_x = m$. Fix a threshold $\phi \in (0, 1)$.

- **Exact heavy hitters.** Output the set $H_\phi = \{x : f_x > \phi m\}$. It has fewer than $1/\phi$ items, because their counts add up to more than $|H_\phi| \phi m$ and to at most $m$.
- **$\varepsilon$-approximate heavy hitters.** For $0 < \varepsilon < \phi$, output a list $L$ such that every $x$ with $f_x > \phi m$ is in $L$, and no $x$ with $f_x < (\phi - \varepsilon) m$ is in $L$. Items in between may or may not be in $L$.
- **With estimates.** Together with $L$, output an estimate $\hat f_x$ for each $x \in L$ with $|\hat f_x - f_x| \le \varepsilon m$.

The problem is close to [frequency estimation](/frequency-estimation/), which asks for $\hat f_x$ with error at most $\varepsilon m$ for any $x$ at query time. An estimator with this error solves the approximate problem. If the estimates are never too large, as in Misra-Gries, report the items with $\hat f_x \ge (\phi - \varepsilon) m$. If they are never too small, as in Space-Saving, report the items with $\hat f_x > \phi m$. If the error is two-sided and at most $\varepsilon m / 2$, report the items with $\hat f_x > (\phi - \varepsilon/2) m$. The only extra work is to find the candidates without a query for each of the $n$ items.

A randomized algorithm must meet the guarantee with probability at least $1 - \delta$, in the sense of the [epsilon-delta guarantee](/epsilon-delta-guarantee/).

## Variants

- **Top $k$.** Output the $k$ items with the largest counts. Exact top $k$ is as hard as exact heavy hitters. The approximate version asks for $k$ items whose counts are each at least $(1 - \varepsilon)$ times the $k$-th largest count.
- **The $\ell_2$ version.** Output the items with $f_x^2 > \phi \sum_y f_y^2$, with error $\varepsilon \|f\|_2$. On skewed data $\|f\|_2$ is much smaller than $\|f\|_1 = m$, so this is a stronger guarantee. The [count sketch](/count-sketch/) solves it.
- **Turnstile streams.** In the [turnstile model](/turnstile-model/) items can be deleted, and the threshold refers to $\|f\|_1$. Counter-based summaries fail here, and linear sketches are the standard answer.
- **Weighted items.** Each item carries a weight, as with bytes in network flows. The counter-based summaries extend to weights, and [sample and hold](/sample-and-hold/) was designed for this case.
- **Sliding windows.** Only the most recent items count, as in [sliding-window heavy hitters](/sliding-window-heavy-hitters/).
- **Majority.** The case $\phi = 1/2$ is the [majority element problem](/majority-element-problem/).

## Examples

Take $\sigma = a, b, a, c, a, b, d, a, b, e$, so $m = 10$ and $f_a = 4$, $f_b = 3$, $f_c = f_d = f_e = 1$.

| $\phi$ | $\varepsilon$ | must report | may report | must not report |
|---|---|---|---|---|
| $0.3$ | exact | $a$ | | all others |
| $0.3$ | $0.05$ | $a$ | $b$ ($f_b = 3 \ge 2.5$, and $3 \not> 3$) | $c, d, e$ |
| $0.2$ | $0.15$ | $a, b$ | $c, d, e$ ($f = 1 \ge 0.5$) | none |
| $0.5$ | exact | none | | all, since $4 \not> 5$ |

In the third row, $\varepsilon$ is so large that every item may be reported. A useful guarantee needs $\varepsilon$ small compared with $\phi$, for example $\varepsilon = \phi/10$.

## Known algorithms

**Counter-based, deterministic, insertion-only.** These keep a small table of items with counters.

- **[Misra-Gries summary](/misra-gries-summary/) (1982).** $k - 1$ counters, decrement all when a new item finds the table full. Each estimate is low by at most $m/k$. With $k = \lceil 1/\varepsilon \rceil$ it uses $O(1/\varepsilon)$ words and $O(1)$ amortized time. The [Boyer-Moore majority vote](/boyer-moore-majority/) is the case $k = 2$.
- **[Space-Saving](/space-saving/) (2005).** $k$ counters, the new item takes over the smallest counter. Each estimate is high by at most $m/k$. It is isomorphic to Misra-Gries with $k - 1$ counters.
- **[Lossy counting](/lossy-counting/) (2002).** Entries with an error term, pruned at the end of each bucket of $\lceil 1/\varepsilon \rceil$ items. Each estimate is low by at most $\varepsilon m$, with $O((1/\varepsilon) \log(\varepsilon m))$ entries in the worst case.

**Sampling-based, randomized, insertion-only.**

- **[Sticky sampling](/sticky-sampling/) (2002).** Sample new items with a rate that falls over time, and count each sampled item exactly from then on. Its memory does not depend on $m$.
- **[Sample and hold](/sample-and-hold/) (2002).** Sample each byte or packet with a fixed probability, and count a flow exactly once it is sampled. It was designed for large flows in network routers.

**Sketch-based, randomized, linear.** These work in the turnstile model and are [linear sketches](/linear-sketch/).

- **[Count-min sketch](/count-min-sketch/) (2005).** $d = \lceil \ln(1/\delta) \rceil$ rows of $w = \lceil e/\varepsilon \rceil$ counters. Each estimate is high by at most $\varepsilon \|f\|_1$ with probability $1 - \delta$, in the cash register model.
- **[Count sketch](/count-sketch/) (2002).** Rows of counters with random signs and a median. The error is at most $\varepsilon \|f\|_2$ with $O((1/\varepsilon^2) \log(1/\delta))$ counters.
- **Finding the candidates.** A sketch answers point queries, but a list needs candidates. In the cash register model, keep a heap of the items whose estimates are above the threshold. In the turnstile model, keep one sketch for each level of [dyadic intervals](/dyadic-intervals/) and search down from the root, only into intervals whose estimated count is above the threshold. This multiplies the space and the update time by $\log n$.

## Bounds

**The exact version needs $\Omega(n)$ bits in one pass.** Even the case $\phi = 1/2$, deciding whether a majority exists, needs $\Omega(n)$ bits for a randomized one-pass algorithm on streams of length $O(n)$. The reduction from INDEX is on the [majority element problem](/majority-element-problem/) page and the [INDEX lower bound](/index-problem-lower-bound/) page.

**Error $\varepsilon m$ needs $\Omega(1/\varepsilon)$ bits.** Let $t = \lfloor 1/(3\varepsilon) \rfloor$. Alice has $x \in \{0, 1\}^t$ and streams each $i$ with $x_i = 1$ once. Bob has an index $j$, and he must learn $x_j$. Alice runs a frequency estimation algorithm with error $\varepsilon m$ on her stream and sends its memory to Bob, who queries $j$. Here $m \le t \le 1/(3\varepsilon)$, so the error is at most $\varepsilon m \le 1/3$, and Bob rounds $\hat f_j$ to get $f_j = x_j$. So the memory is a one-way protocol for INDEX on $t$ bits, and by the [INDEX lower bound](/index-problem-lower-bound/) it has $\Omega(t) = \Omega(1/\varepsilon)$ bits, also for randomized algorithms with error probability $1/3$.

**Upper bounds.** The counter-based summaries use $O(1/\varepsilon)$ words, that is $O((1/\varepsilon)(\log n + \log m))$ bits, so they are optimal up to the size of a word. The count-min sketch uses $O((1/\varepsilon) \log(1/\delta))$ words for point queries, and the count sketch $O((1/\varepsilon^2) \log(1/\delta))$ words for the stronger $\ell_2$ guarantee.

## Reductions

- **From frequency estimation.** An estimator with additive error $\varepsilon m$ and a way to list candidates gives the approximate heavy hitters, as in the definition.
- **From the majority element problem.** Majority is the case $\phi = 1/2$.
- **From INDEX.** As in the bounds above, INDEX reduces to both the exact version and the approximate version with error $\varepsilon m$.
- **To the second pass.** On stored data, any list of candidates that contains $H_\phi$, for example the counters of Misra-Gries with $k = \lceil 1/\phi \rceil$, gives $H_\phi$ exactly after a second pass that counts the candidates.

## Applications

- **Network monitoring.** Find the flows or sources that use more than a fraction of the bandwidth, for traffic engineering, billing and the detection of attacks.
- **Search and advertising.** Find popular queries, and frequent clicks or fraudulent click patterns.
- **Databases.** Answer iceberg queries, which ask for the groups with an aggregate above a threshold, and estimate the skew of a join attribute for query planning.
- **Association rules.** Frequent item sets in market basket data start with frequent single items. Manku and Motwani used lossy counting for this.
- **Caches.** Keep the hot keys of a cache or of a shard.

## References
