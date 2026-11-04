---
tag: PXRDWM
kind: problem
slug: frequency-estimation
name: Frequency estimation problem
aliases:
- point query
- item frequency estimation
area: data-structures/probabilistic-structures
level: core
summary: Estimate how many times each item occurs in a stream or multiset.
prereqs: [streaming-model, frequency-vector, turnstile-model]
see_also: [count-min-sketch, count-sketch, misra-gries-summary, space-saving, frequent-items-problem, count-min-error-bound, spectral-bloom-filter, index-problem]
sources:
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pages 58 to 75 (the point query, the count-min sketch and the reductions to range queries, quantiles and heavy hitters)
  - paper: doi:10.1016/0167-6423(82)90012-0
    title: Jayadev Misra and David Gries, Finding repeated elements, Science of Computer Programming 2(2), 1982
    locator: pages 143 to 152 (the deterministic algorithm with k counters)
  - paper: doi:10.1016/s0304-3975(03)00400-6
    title: Moses Charikar, Kevin Chen and Martin Farach-Colton, Finding frequent items in data streams, Theoretical Computer Science 312(1), 2004
    locator: pages 3 to 15 (the count sketch and the error in terms of the second norm)
  - paper: doi:10.1007/s000370050018
    title: Ilan Kremer, Noam Nisan and Dana Ron, On randomized one-round communication complexity, Computational Complexity 8, 1999
    locator: pages 21 to 49 (the one-way communication lower bound for the index function)
  - paper: doi:10.1145/964725.633056
    title: Cristian Estan and George Varghese, New directions in traffic measurement and accounting, SIGCOMM 2002
    locator: pages 323 to 336 (counting the traffic of large flows in routers)
---

The frequency estimation problem asks for a small summary of a stream of items that can answer, for any item $x$, about how many times $x$ has occurred. The answer may be off by at most $\varepsilon N$, where $N$ is the length of the stream, or by $\varepsilon$ times the second norm of the counts. Exact counts need memory for each distinct item, but an additive error of $\varepsilon N$ is possible in $O(1/\varepsilon)$ counters, independent of the number of distinct items. It is the core problem behind the [count-min sketch](/count-min-sketch/), the [Misra-Gries summary](/misra-gries-summary/) and the search for [frequent items](/frequent-items-problem/).

## In plain words

A router sees millions of packets each second, and its owner wants to know how much traffic each customer sends. A full table with one counter for each customer does not fit in the fast memory of the router.

The question changes to this: for any one customer, give the count to within one percent of all traffic. A small customer may get an answer of "about zero", which is fine. A large customer gets a count that is close, compared with the total.

This weaker promise can be met with a fixed number of counters, a few hundred or a few thousand, however many customers there are. Some methods never count too much, some never count too little, and the random ones are right with high probability.

## Definition

Let the items come from a universe $U = \{1, \ldots, u\}$. A stream is a sequence of updates $(x_t, c_t)$ with $x_t \in U$, and it defines the [frequency vector](/frequency-vector/) $f \in \mathbb{Z}^u$ with $f_x = \sum_{t : x_t = x} c_t$.

- In the *cash register* model each $c_t = 1$ (or $c_t > 0$), so $f \ge 0$ and $N = \|f\|_1 = \sum_x f_x$ is the number of updates.
- In the *strict turnstile* model $c_t$ may be negative but $f \ge 0$ at all times, as with inserts and deletes of a multiset.
- In the general [turnstile model](/turnstile-model/) $f$ may have negative entries.

A summary with parameters $\varepsilon, \delta \in (0, 1)$ solves the **point query** problem with the $\ell_1$ guarantee if, after any stream, a query for any $x \in U$ returns $\hat f_x$ with
$$ \Pr\left[\,|\hat f_x - f_x| \le \varepsilon \|f\|_1\,\right] \ge 1 - \delta. $$
The guarantee is for each fixed query; it does not say that all $u$ answers are good at the same time. The **$\ell_2$ guarantee** replaces $\|f\|_1$ by $\|f\|_2 = (\sum_x f_x^2)^{1/2}$, which is never larger and is much smaller when the counts are spread out. A summary is **deterministic** if $\delta = 0$. It has **one-sided error** if $\hat f_x \ge f_x$ always, or $\hat f_x \le f_x$ always.

The measure of cost is the memory of the summary in words or bits, and the time for an update and a query.

## Variants

- **Overestimate or underestimate.** The count-min sketch never underestimates in the strict turnstile model. The Misra-Gries summary never overestimates. [Space-saving](/space-saving/) never underestimates.
- **The tail guarantee.** Let $f^{\text{res}(k)}$ be $f$ with its $k$ largest entries set to 0. Several summaries guarantee error $\varepsilon \|f^{\text{res}(k)}\|_1$ with $k = O(1/\varepsilon)$, which is much better on skewed data, where a few items carry most of the weight.
- **Heavy hitters.** The [frequent items problem](/frequent-items-problem/) asks for all $x$ with $f_x \ge \phi N$, without knowing them in advance. It is the main use of frequency estimation.
- **Sets with counts.** In the static version the multiset is given at once, as for the [spectral Bloom filter](/spectral-bloom-filter/). Then the answer for each $x$ outside the multiset is also asked to be 0 with high probability.
- **Weighted and sliding windows.** The updates have weights, or only the last $W$ updates count.

## Examples

Let the stream be a b a c a b d a. Then $N = 8$ and $f_a = 4$, $f_b = 2$, $f_c = 1$, $f_d = 1$. With $\varepsilon = 1/3$, each estimate may be off by $8/3$.

**Misra-Gries with 2 counters.** Keep at most 2 items with counters. On a new item with no free counter, decrement all counters and drop those at 0.

| item | a | b | a | c | a | b | d | a |
|---|---|---|---|---|---|---|---|---|
| counters | a:1 | a:1 b:1 | a:2 b:1 | a:1 | a:2 | a:2 b:1 | a:1 | a:2 |

The estimates are $\hat f_a = 2$ and $\hat f_b = \hat f_c = \hat f_d = 0$. Each is at most the true count and at most 2 less. There were 2 decrement steps, and each removed 3 occurrences from the count: the 2 counters and the new item. So the error is at most $N/3$.

**Count-min with one row of 3 counters.** Let a hash function send a and c to counter 0, b to counter 1 and d to counter 2. The counters are $[5, 2, 1]$. The estimates are $\hat f_a = \hat f_c = 5$, $\hat f_b = 2$ and $\hat f_d = 1$. They are never too small; c is too large by 4 because it shares a counter with a. More rows with independent hash functions, and the minimum over the rows, make such collisions unlikely; see the [count-min error bound](/count-min-error-bound/).

## Known algorithms

| summary | model | space in counters | guarantee | error |
|---|---|---|---|---|
| exact table | turnstile | number of distinct items | exact | 0 |
| [Misra-Gries](/misra-gries-summary/) (1982) | cash register | $1/\varepsilon$ | deterministic, $\ell_1$ | underestimate |
| [space-saving](/space-saving/) | cash register | $1/\varepsilon$ | deterministic, $\ell_1$ | overestimate |
| [lossy counting](/lossy-counting/) | cash register | $(1/\varepsilon) \log(\varepsilon N)$ | deterministic, $\ell_1$ | underestimate |
| [count-min sketch](/count-min-sketch/) | strict turnstile | $(e/\varepsilon) \ln(1/\delta)$ | randomized, $\ell_1$ | overestimate |
| [count sketch](/count-sketch/) | turnstile | $O(\varepsilon^{-2} \log(1/\delta))$ | randomized, $\ell_2$ | two-sided |
| [spectral Bloom filter](/spectral-bloom-filter/) | strict turnstile | $O(n)$ for $n$ distinct items | randomized | overestimate |

In the deterministic summaries a counter also stores an item, so it is $O(\log u + \log N)$ bits. In the sketches a counter stores only a count, and the hash functions take $O(\log u)$ bits each.

## Bounds

**Exact counting.** Exact frequencies of a stream over $U$ need $\Omega(\min(u, N))$ bits: from the exact frequencies one can read back any subset of $\{1, \ldots, \min(u, N)\}$, and there are $2^{\min(u, N)}$ of them.

**The $\ell_1$ lower bound.** Each randomized summary with the $\ell_1$ guarantee and $\delta \le 1/3$ needs $\Omega(1/\varepsilon)$ bits, by a reduction from the [index problem](/index-problem/). Let $t$ be an integer with $t < 1/(2\varepsilon)$. Alice holds $z \in \{0, 1\}^t$ and feeds the stream of the $i$ with $z_i = 1$, so $N \le t$ and $\varepsilon N < 1/2$. She sends the summary to Bob, who queries his index $i$. The answer is within less than $1/2$ of $f_i = z_i$ with probability $2/3$, so Bob learns $z_i$. Kremer, Nisan and Ron (1999) proved that the one-way randomized communication of the index function on $t$ bits is $\Omega(t)$, so the summary has $\Omega(1/\varepsilon)$ bits. With items of $\log_2 u$ bits and counts up to $N$, the Misra-Gries summary uses $O((1/\varepsilon)(\log u + \log N))$ bits.

**Count-min.** The [count-min error bound](/count-min-error-bound/) shows that $\lceil e/\varepsilon \rceil \cdot \lceil \ln(1/\delta) \rceil$ counters suffice for the $\ell_1$ guarantee with one-sided error in the strict turnstile model.

## Reductions

- **Heavy hitters from point queries.** In the cash register model, keep a point query summary and a list of the items whose estimate is at least $\phi N$, updated as items arrive. In the turnstile model, put a summary on each level of the [dyadic intervals](/dyadic-intervals/) of $U$ and search from the root down, keeping only the intervals with estimate at least $\phi N$.
- **Range queries and quantiles.** A range $[a, b]$ is the disjoint union of $O(\log u)$ dyadic intervals, so point queries on all levels answer range sums with error $O(\varepsilon N \log u)$, and binary search on prefix sums gives approximate [quantiles](/quantile-summary-problem/).
- **Inner products.** Count-min sketches of two streams with the same hash functions estimate $\sum_x f_x g_x$, the size of a join, with error $\varepsilon \|f\|_1 \|g\|_1$, which solves the [join size estimation problem](/join-size-estimation-problem/) approximately.
- **From the index problem.** The lower bound above reduces the [index problem](/index-problem/) to point queries.

## Applications

- Network measurement: the traffic of large flows in a router, as proposed by Estan and Varghese (2002), and the detection of heavy sources in attacks.
- Databases: estimates of the number of rows with a given value for the query optimizer, iceberg queries, and join sizes.
- Search engines and logs: the most frequent queries or terms of a day.
- Caches: [cache admission policies](/cache-admission-policy/) that let a new object into the cache only if its estimated frequency beats that of the object it would replace.
- Natural language processing: approximate counts of word pairs and other $n$-grams in large text collections.

## References
