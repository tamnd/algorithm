---
tag: 3V56B1
kind: problem
slug: variable-size-caching
name: Caching with variable object sizes
aliases:
- generalized caching
- file caching problem
- caching with object sizes
area: systems/caching-policies
level: advanced
summary: "Caching where each object has its own size and miss cost. Offline it is strongly NP-hard even when each miss costs 1, and Belady's rule is no longer optimal."
prereqs: [cache, paging-problem, belady-optimal, np-hard]
see_also: [greedy-dual, gdsf, landlord-algorithm, weighted-paging-problem, cache-admission-policy, cache-hit-ratio, knapsack-problem, strong-np-hardness]
sources:
  - paper: doi:10.1007/s00453-011-9502-9
    title: "Marek Chrobak, Gerhard J. Woeginger, Kazuhisa Makino and Haifeng Xu, Caching is hard, even in the fault model, Algorithmica 63(4) (2012), 781-794"
    locator: strong NP-completeness of offline caching with multi-size pages in the fault model and in the bit model, under the forced and the optional policy; the conference version is ESA 2010
  - paper: doi:10.1007/s00453-016-0185-0
    title: "Lukáš Folwarczný and Jiří Sgall, General caching is hard: even with small pages, Algorithmica 79(2) (2017)"
    locator: the abstract and introduction (strong NP-hardness with page sizes in 1, 2, 3, in the fault and bit models; the earlier proofs needed pages larger than half the cache)
  - paper: "Amotz Bar-Noy, Reuven Bar-Yehuda, Ari Freund, Joseph Naor and Baruch Schieber, A unified approach to approximating resource allocation and scheduling, Journal of the ACM 48(5) (2001), 1069-1090"
    title: "Bar-Noy, Bar-Yehuda, Freund, Naor and Schieber, A unified approach to approximating resource allocation and scheduling, JACM 2001"
    locator: the local ratio method and its application to general caching, a 4-approximation of the offline optimum
  - paper: doi:10.1007/s00453-001-0124-5
    title: "Neal E. Young, On-line file caching, Algorithmica 33(3) (2002), 371-383"
    locator: the file caching model (sizes and retrieval costs) and the Landlord algorithm with ratio k/(k - h + 1)
  - paper: "Daniel S. Berger, Nathan Beckmann and Mor Harchol-Balter, Practical bounds on optimal caching with variable object sizes, Proceedings of the ACM on Measurement and Analysis of Computing Systems 2(2) (2018), SIGMETRICS 2018"
    title: "Berger, Beckmann and Harchol-Balter, Practical bounds on optimal caching with variable object sizes, POMACS 2(2), 2018"
    locator: the flow-based offline bounds (FOO) on the optimal miss ratio of real traces with variable object sizes
---

Caching with variable object sizes is the [paging problem](/paging-problem/) in which each object $x$ has a size $s(x)$ and a miss cost $c(x)$, and the cache holds objects of total size at most $k$. The goal is to serve a request sequence with the least total miss cost. With unit sizes and unit costs it is plain paging, where [Belady's rule](/belady-optimal/) is optimal; with different sizes the offline problem is strongly [NP-hard](/np-hard/), even when each miss costs 1. Web caches, CDNs, key-value stores and file caches all face this problem, because their objects range from a few bytes to many megabytes.

## In plain words

A cache has a fixed number of bytes. Each object takes some bytes, and loading it after a miss has a price. The price can be the same for each object, it can grow with the size, or it can be anything, such as the time to reach a far server.

When a new object does not fit, the cache must throw out enough bytes to make room. With objects of one size, the best choice is easy if you know the future: throw out the object needed last. With mixed sizes this choice goes wrong. Throwing out one big object may free the room of three small ones, and the object needed last may be too small to free enough room on its own. Which set of objects to throw out becomes a puzzle like packing a bag, and no fast exact method is known.

## Definition

**Input.** A capacity $k \ge 1$. A set of objects; each object $x$ has a size $s(x) \in \{1, \ldots, k\}$ and a cost $c(x) \ge 0$. A request sequence $\sigma = \sigma_1 \cdots \sigma_n$ of objects.

**Policy.** A policy keeps a cache $C_t$ after request $t$, with $C_0 = \emptyset$ and $\sum_{x \in C_t} s(x) \le k$ for each $t$. Request $t$ is a *hit* if $\sigma_t \in C_{t-1}$ and a *miss* otherwise.

- In the **forced** model, $\sigma_t \in C_t$ for each $t$: a missed object must be loaded.
- In the **optional** model (also called caching with *bypass*), a miss may be served without loading $\sigma_t$, so $C_t \subseteq C_{t-1} \cup \{\sigma_t\}$ with no other condition.

**Goal.** Minimize the total miss cost $\sum_{t\,:\,\sigma_t \notin C_{t-1}} c(\sigma_t)$. The *offline* problem knows $\sigma$ in advance. The *online* problem learns $\sigma_t$ only at time $t$, and is judged by its [competitive ratio](/competitive-ratio/).

**Cost models.** The names come from the literature on [weighted paging](/weighted-paging-problem/):

| model | cost $c(x)$ | what the total counts | the measure in systems |
|---|---|---|---|
| fault model | $1$ | the number of misses | object miss ratio |
| bit model | $s(x)$ | the bytes loaded after misses | byte miss ratio |
| general model | any $c(x) \ge 0$ | latency, money or load on the origin | cost miss ratio |

The two common hit ratios on the [cache hit ratio](/cache-hit-ratio/) page are the fault model and the bit model. One policy can be good in one model and poor in the other: keeping many small objects raises the object hit ratio and lowers the byte hit ratio.

## Variants

- **Unit sizes, any costs.** This is [weighted paging](/weighted-paging-problem/). The offline optimum is a minimum-cost flow, so it is polynomial. Its online algorithm is [GreedyDual](/greedy-dual/).
- **Unit sizes and unit costs.** Plain [paging](/paging-problem/). Belady's MIN is optimal offline, and [LRU](/lru/) is $k$-competitive online.
- **Forced and optional.** The optional model lets a cache refuse to admit an object. An [admission policy](/cache-admission-policy/) such as [TinyLFU](/tinylfu/) is the online form of this choice. With sizes, admission matters more than with unit sizes, because one large object can push out many small ones.
- **Resource augmentation.** Compare an online cache of size $k$ with an optimum of size $h \le k$. This gives the ratio $k/(k - h + 1)$ of the [Landlord](/landlord-algorithm/) algorithm.

## Examples

**Belady's rule is not optimal.** Take the capacity $k = 3$, the objects $a$ of size 1 and $b, c$ of size 2, and the trace $a\,b\,c\,b\,a$. The rule "while the new object does not fit, evict the object whose next request is furthest" runs as follows.

| $t$ | request | result | evicted | cache after |
|---|---|---|---|---|
| 1 | $a$ | miss | | $\{a\}$ |
| 2 | $b$ | miss | | $\{a, b\}$ |
| 3 | $c$ | miss | $a$ (next use at 5), then $b$ (next use at 4) | $\{c\}$ |
| 4 | $b$ | miss | $c$ (never used again) | $\{b\}$ |
| 5 | $a$ | miss | | $\{a, b\}$ |

At time 3 the object $c$ needs 2 free units and only 0 are free. Belady's rule evicts $a$ first, because $a$ is needed last. That frees only 1 unit, so the rule also evicts $b$. The optimum evicts only $b$, keeps $a$, misses on $b$ at time 4 (evicting $c$) and hits on $a$ at time 5. So the optimum has 4 misses and Belady's rule has 5 in the fault model. In the bit model the costs are 7 and 8. An exhaustive search over all eviction choices gives the same optimum values, 4 and 7.

**Bypass helps.** Take $k = 2$, the objects $a, b$ of size 1 and $z$ of size 2, and the trace $a\,b\,z\,a\,b$, fault model. In the forced model $z$ must enter, so it evicts both $a$ and $b$, and all 5 requests miss. In the optional model the cache serves $z$ without loading it, and only the first $a$, the first $b$ and $z$ miss: the cost is 3.

**Unit sizes.** With all sizes and costs equal to 1, exhaustive search and Belady's rule give the same number of misses on each of 300 random traces with seed 7. This is the theorem on the [Belady optimality](/belady-optimality/) page; the example above shows that it needs the sizes to be equal.

## Known algorithms

- **Exact search.** A dynamic program over the set of cached objects after each request gives the offline optimum. It takes time exponential in the number of distinct objects, and is useful only to check other methods on small traces.
- **[GreedyDual-Size](/greedy-dual/)** (Cao and Irani 1997) and **[Landlord](/landlord-algorithm/)** (Young 2002): the online rule with priority $L + c(x)/s(x)$. It is $k$-competitive, where $k$ is the capacity in units of the smallest size.
- **[GDSF](/gdsf/)**: GreedyDual-Size with a frequency count in the priority, for web proxies.
- **Size-aware heuristics.** Evict the largest object first, or use [LRU](/lru/) with an admission rule. These have no worst-case guarantee in the general model.
- **Offline approximations.** The local ratio method of Bar-Noy, Bar-Yehuda, Freund, Naor and Schieber gives a 4-approximation of the offline optimum in the general model.
- **Practical offline bounds.** For a long real trace even a 4-approximation is too loose to judge a policy. Berger, Beckmann and Harchol-Balter (2018) compute upper and lower bounds on the optimal miss ratio from a minimum-cost flow model of the trace (FOO), and report that the two bounds are close on production traces.

## Bounds

- **Offline, unit sizes.** Polynomial: Belady's MIN for unit costs, a minimum-cost flow for any costs.
- **Offline, variable sizes.** Chrobak, Woeginger, Makino and Xu (2012) prove that the problem is strongly NP-complete in the fault model and in the bit model, in both the forced and the optional form. The fault model had been open since the 1990s. Their reduction uses objects larger than half of the cache. Folwarczný and Sgall (2017) show strong NP-hardness even when all sizes are in $\{1, 2, 3\}$. So no pseudo-polynomial algorithm exists unless P = NP (see [strong NP-hardness](/strong-np-hardness/)).
- **Offline approximation.** A 4-approximation exists (Bar-Noy et al. 2001). Folwarczný and Sgall state that no hardness of approximation result was known when they wrote.
- **Online, deterministic.** Landlord and GreedyDual-Size are $k$-competitive, and $k/(k - h + 1)$-competitive against an optimum with capacity $h \le k$ (Young 2002). The [lower bound $k$ for deterministic paging](/sleator-tarjan-paging-bound/) is a special case, so the ratio is tight.
- **Online, randomized.** The best known ratio is $O(\log k)$; see the [weighted paging](/weighted-paging-problem/) page for the history.

## Reductions

- **Paging is a special case.** Set each size and each cost to 1. So each lower bound for [paging](/paging-problem/) holds here.
- **A step like knapsack.** At one miss, choose which objects to keep, with total size at most $k - s(\sigma_t)$, to save the most future cost. This choice has the form of a [knapsack problem](/knapsack-problem/), and it explains why rules that rank objects one at a time, as Belady's rule does, can fail. The NP-hardness proofs above use a different and more complex reduction, because one step alone does not decide the cost of the whole sequence.

## Applications

- **Web proxies and CDNs.** Objects differ in size by several orders of magnitude, and the origin cost differs by server. GreedyDual-Size and GDSF were designed for this case.
- **Key-value caches.** Memcached and similar stores hold values of many sizes. A miss costs a database query, so the general model fits.
- **File and storage caches.** Whole-file caches use the file size; block caches have unit sizes, and so are plain paging.
- **Judging a policy.** The offline optimum, or its FOO bounds, tells how far a policy is from the best possible on a trace. Belady's rule is a wrong reference here, because it is not optimal with sizes.

## References
