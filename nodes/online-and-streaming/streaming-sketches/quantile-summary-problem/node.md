---
tag: 6EP9F6
kind: problem
slug: quantile-summary-problem
name: Quantile summary problem
aliases:
- approximate quantiles
- order statistics in a stream
- epsilon-approximate quantile summary
area: online-and-streaming/streaming-sketches
level: core
summary: Keep a small summary of a stream that answers every rank or quantile query within εn in rank, and find how small such a summary can be.
prereqs: [order-statistic, selection-problem, streaming-model, epsilon-delta-guarantee]
see_also: [greenwald-khanna-summary, kll-sketch, q-digest, t-digest, munro-paterson-algorithm, dyadic-intervals, mergeable-summaries, sliding-window-quantiles]
sources:
  - paper: doi:10.1016/0304-3975(80)90061-4
    title: J. Ian Munro and Mike S. Paterson, Selection and sorting with limited storage, Theoretical Computer Science 12(3), 1980
    locator: pp. 315 to 323 (Theorem 4, the lower bound Ω(n^(1/p)) for p-pass exact selection)
  - paper: doi:10.1145/375663.375670
    title: Michael Greenwald and Sanjeev Khanna, Space-efficient online computation of quantile summaries, SIGMOD 2001
    locator: pp. 58 to 66 (the definition of an ε-approximate quantile summary and the O((1/ε) log(εn)) summary)
  - url: https://arxiv.org/abs/1905.03838
    title: Graham Cormode and Pavel Veselý, A tight lower bound for comparison-based quantile summaries, PODS 2020
    locator: the main theorem, Ω((1/ε) log(εn)) items for deterministic comparison-based summaries
  - url: https://arxiv.org/abs/1603.05346
    title: Zohar Karnin, Kevin Lang and Edo Liberty, Optimal quantile approximation in streams, FOCS 2016
    locator: Theorem 5 (the upper bound O((1/ε) log log(1/δ))) and Theorem 6 (the matching lower bound for randomized comparison-based algorithms)
  - paper: doi:10.1145/2213556.2213562
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, PODS 2012
    locator: the section on quantiles (one-way mergeability of GK, the randomized mergeable summary, and the open question for GK)
  - url: https://arxiv.org/abs/2404.03847
    title: Meghal Gupta, Mihir Singhal and Hongxun Wu, Optimal quantile estimation, beyond the comparison model, FOCS 2024
    locator: the main theorem (a deterministic sketch of O(1/ε) words for integer items)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 4, Summaries for Ordered Data
---

The quantile summary problem asks for a small summary of a stream of $n$ ordered items that can answer, at any time, a question such as "which item is at rank $r$?" or "what is the median?" with an error of at most $\varepsilon n$ in rank. An exact answer needs $\Omega(n)$ memory in one pass, so the problem allows this additive error. The central questions are how much space a summary needs as a function of $\varepsilon$ and $n$, whether randomness helps, and whether summaries of two streams can be merged. On this page $n$ is the stream length, $U$ is the size of the universe when the items are integers, and the stream $\sigma$ is insertion only unless the text says otherwise.

## In plain words

A web service logs the response time of every request, and the team wants the median and the slowest one percent. Sorting all of the times is too costly, and the times keep coming. A quantile summary keeps a few hundred numbers instead of millions. When you ask for the median, it gives a number that is close to the true median in position: if there are a million times and the error is one in a thousand, the answer is somewhere between position 499,000 and 501,000. The problem is to keep this promise for every question with as little memory as possible.

## Definition

**Ranks.** Let $\sigma = x_1, \ldots, x_n$ be the items so far, from a totally ordered set. For a value $v$, let $R(v) = |\{i : x_i \le v\}|$ be its rank. When values repeat, a value $v$ covers the range of positions $(R(v^-), R(v)]$, where $R(v^-) = |\{i : x_i < v\}|$.

**Quantile query.** For $\phi \in (0, 1]$, an exact $\phi$-quantile is an item at position $\lceil \phi n \rceil$ in sorted order. An $\varepsilon$-approximate $\phi$-quantile is an item $v$ whose range of positions meets $[(\phi - \varepsilon)n, (\phi + \varepsilon)n]$.

**Rank query.** For a value $v$, return $\hat R(v)$ with $|\hat R(v) - R(v)| \le \varepsilon n$. For summaries that store items, the two kinds of query are equivalent up to a factor 2 in $\varepsilon$.

**The problem.** Process $\sigma$ in one pass and keep a summary $S$. At any time, $S$ must answer quantile or rank queries with error $\varepsilon n$. A summary is

- **deterministic** if it answers every query correctly, always;
- **randomized for all queries** if, with probability at least $1 - \delta$, it answers all queries at once correctly;
- **randomized for each query** if each fixed query is correct with probability at least $1 - \delta$.

**Comparison-based.** A summary is comparison-based if it stores items of the stream, uses them only through comparisons, and answers quantile queries with stored items. GK, KLL and the Munro-Paterson method are comparison-based. The q-digest is not, since it uses the binary digits of integer items.

**Space.** Space is counted in words or in stored items. One word holds one item or one count up to $n$.

## Variants

- **Exact selection with few passes.** Find the exact item of rank $r$ with $p$ passes over the data. This is the setting of the [Munro-Paterson algorithm](/munro-paterson-algorithm/).
- **Relative error.** Ask for error $\varepsilon R(v)$ instead of $\varepsilon n$, so that the tails are more accurate. This needs more space; see the [KLL sketch](/kll-sketch/) page for the variants.
- **Turnstile streams.** Items can also be deleted ([turnstile model](/turnstile-model/)). A summary that stores items cannot handle deletions, and one uses [linear sketches](/linear-sketch/) over [dyadic intervals](/dyadic-intervals/) instead.
- **Sliding windows.** Answer queries over the last $W$ items; see [sliding window quantiles](/sliding-window-quantiles/).
- **Mergeable summaries.** Build summaries of parts of the data on many machines and combine them into a summary of the union with the same error and space; see [mergeable summaries](/mergeable-summaries/).
- **Weighted items.** Each item has a weight, and ranks are sums of weights.

## Examples

**One query.** Let $\sigma$ be a permutation of $1, \ldots, 20$, so $n = 20$, and let $\varepsilon = 0.1$, so $\varepsilon n = 2$. The exact median is the item at position 10, which is 10. An $\varepsilon$-approximate median is any item at a position in $[8, 12]$, so each of 8, 9, 10, 11 and 12 is a correct answer. The [GK summary](/greenwald-khanna-summary/) page traces a stream of this kind with 7 stored tuples, and its median query returns 12.

**Repeated values.** Let $\sigma$ be 5, 5, 5, 5, 1, 9 with $\varepsilon = 0.2$, so $\varepsilon n = 1.2$. The value 5 covers the positions 2 to 5. For $\phi = 1/6$, the target position is 1 and the allowed range is $[-0.2, 2.2]$, which meets the positions of 1 and of 5. So both 1 and 5 are correct answers, but 9 is not.

**The offline summary.** If all of the data is known and sorted, the items at positions 10, 30, 50, and so on up to 990 answer every query for $n = 1000$ and $\varepsilon = 0.01$: each position from 1 to 1000 is within 10 of one of them. That is $1/(2\varepsilon) = 50$ items. In a stream the final positions are not known until the end, and the lower bounds below show that this costs a factor $\log(\varepsilon n)$ for deterministic comparison-based summaries.

## Known algorithms

| summary | stream model | guarantee | space |
|---|---|---|---|
| store everything and sort | any | exact | $n$ words |
| [Munro-Paterson](/munro-paterson-algorithm/), $p$ passes | insertion only | exact selection | $O(n^{1/p} \log^{2 - 2/p} n)$ words |
| Manku, Rajagopalan and Lindsay 1998 | insertion only, $n$ known | deterministic | $O((1/\varepsilon)\log^2(\varepsilon n))$ items |
| [GK summary](/greenwald-khanna-summary/) | insertion only | deterministic | $O((1/\varepsilon)\log(\varepsilon n))$ items |
| [q-digest](/q-digest/) | insertion only, integers in $[0, U)$ | deterministic, mergeable | $O((1/\varepsilon)\log U)$ words |
| [KLL sketch](/kll-sketch/) | insertion only | randomized, mergeable | $O((1/\varepsilon)\log^2\log(1/\delta))$ items, or $O((1/\varepsilon)\log\log(1/\delta))$ not mergeable |
| dyadic [Count-Min](/count-min-sketch/) | turnstile, integers | randomized, linear | $O((1/\varepsilon)\log^2 U \log(\log U/\delta))$ words |
| Gupta, Singhal and Wu 2024 | insertion only, integers | deterministic | $O(1/\varepsilon)$ words when $n \le \mathrm{poly}(U)$ |
| [t-digest](/t-digest/) | insertion only | no worst-case guarantee | about $\delta$ centroids for compression $\delta$ |

The dyadic Count-Min row keeps one [Count-Min sketch](/count-min-sketch/) for each of the $\log U$ levels of the [dyadic intervals](/dyadic-intervals/), each with width $O(\log U/\varepsilon)$, so that a prefix count, which is a sum of at most $\log U$ sketch answers, has total error $\varepsilon n$.

## Bounds

**Exact answers need linear space.** Munro and Paterson (Theorem 4) proved that each $p$-pass algorithm that finds the exact median needs $\Omega(n^{1/p})$ words of storage. For $p = 1$ this is $\Omega(n)$, so a one-pass summary must allow error.

**Comparison-based summaries need $\Omega(1/\varepsilon)$ items.** Here is the proof, which also holds for randomized summaries that are correct for all queries at once with positive probability. Take $n$ distinct items and the positions $r_k = (2k - 1)\lceil \varepsilon n + 1 \rceil$ for $k = 1, \ldots, K$, as long as $r_K \le n$. The allowed ranges $[r_k - \varepsilon n, r_k + \varepsilon n]$ are pairwise disjoint, since consecutive centers are more than $2\varepsilon n$ apart. A comparison-based summary answers each query with a stored item, so it must store at least one item in each range, which is $K = \Omega(1/\varepsilon)$ items when $\varepsilon n \ge 1$.

**Deterministic comparison-based summaries need $\Omega((1/\varepsilon)\log(\varepsilon n))$ items.** Hung and Ting (2010) proved $\Omega((1/\varepsilon)\log(1/\varepsilon))$. Cormode and Veselý (2020) proved $\Omega((1/\varepsilon)\log(\varepsilon n))$, which matches the GK summary. Their adversary builds a stream in which any summary that keeps fewer items has two streams with the same summary but with ranks that differ by more than $2\varepsilon n$ for some item.

**Randomized comparison-based summaries.** Karnin, Lang and Liberty (Theorem 6) proved that a randomized comparison-based algorithm that returns an $\varepsilon$-approximate quantile with probability $1 - \delta$ needs $\Omega((1/\varepsilon)\log\log(1/\delta))$ items. Their Theorem 5 gives a matching upper bound. With constant $\delta$, the randomized bound is $\Theta(1/\varepsilon)$, a factor $\log(\varepsilon n)$ below the deterministic one.

**Beyond comparisons.** For integer items from $[0, U)$, the q-digest uses $O((1/\varepsilon)\log U)$ words, and Gupta, Singhal and Wu (2024) reach $O(1/\varepsilon)$ words when $n \le \mathrm{poly}(U)$, below the comparison lower bound.

**Mergeability.** Agarwal et al. (2012) showed that the q-digest is mergeable and gave a randomized mergeable summary of $O((1/\varepsilon)\log^{3/2}(1/\varepsilon))$ items; the KLL sketch with equal top capacities is also mergeable. The GK summary is only one-way mergeable: merging the smaller summary into the larger keeps the error but costs a factor $\log(\varepsilon n)$ in space. Whether a deterministic comparison-based summary can be fully mergeable with $O((1/\varepsilon)\log(\varepsilon n))$ items is an open question.

## Reductions

- **Selection.** A summary with $\varepsilon n < 1$ answers exact [selection](/selection-problem/) queries, so the exact lower bound above transfers. A few passes with an approximate summary narrow the range of an exact [order statistic](/order-statistic/), which is the idea of Munro and Paterson.
- **From rank queries to quantiles.** Given a rank oracle with error $\varepsilon n$ and items from $[0, U)$, a [binary search](/binary-search/) over the values answers a quantile query with error $\varepsilon n$ in $\log U$ calls. This is how dyadic Count-Min answers quantiles.
- **From quantiles to range counts.** The number of items in $[a, b]$ is $R(b) - R(a^-)$, so two rank queries give it with error $2\varepsilon n$.
- **Frequent items.** A value with frequency above $3\varepsilon n$ covers more than $3\varepsilon n$ consecutive positions, so for some multiple $r$ of $\varepsilon n$ the whole range $[r - \varepsilon n, r + \varepsilon n]$ lies inside them, and the query at $r$ must return that value. So $1/\varepsilon$ quantile queries find all [frequent items](/frequent-items-problem/) with threshold $3\varepsilon n$.

## Applications

- Latency monitoring: the 99th and 99.9th percentiles of response times in services.
- Database systems: equi-depth histograms for query planning, and approximate percentile functions in SQL engines.
- Load balancing and partitioning: split points for range partitioning of keys across machines, for example in parallel sort.
- Sensor networks: the q-digest was designed to compute medians over a network with small messages.

## References
