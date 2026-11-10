---
tag: N1ETXA
kind: definition
slug: page-fault
name: Page fault
aliases:
- cache miss
- fault
- miss
area: online-and-streaming/paging-and-caching-online
level: intro
summary: A request for a page that is not in the cache, forcing a fetch and possibly an eviction.
prereqs: [cache]
see_also: [paging-problem, demand-paging, cache-hit-ratio, belady-algorithm, three-cs-model, miss-ratio-curve]
sources:
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, the paging model and its cost (Section 3.1)
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging model, where the cost of a rule is its number of page faults
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the count of page loads as the measure of a replacement algorithm
---

A page fault is a request for a page that is not in the cache at the moment of the request. In the [paging problem](/paging-problem/) a fault costs 1 and a request for a page in the cache, a *hit*, costs 0, so the cost of an algorithm is its number of faults. In hardware caches the same event is called a *cache miss*, and in an operating system the fault is the trap that loads the page from disk.

## Definition

Let $\sigma = \sigma_1 \cdots \sigma_n$ be a request sequence and let $C_{t-1}$ be the set of pages in the cache of an algorithm $A$ just before request $t$, with $|C_{t-1}| \le k$. Request $t$ is a **fault** of $A$ if $\sigma_t \notin C_{t-1}$, and a **hit** if $\sigma_t \in C_{t-1}$. The number of faults of $A$ on $\sigma$ is

$$A(\sigma) = \bigl|\{\, t \in \{1, \ldots, n\} : \sigma_t \notin C_{t-1} \,\}\bigr|.$$

On a fault, a [demand paging](/demand-paging/) algorithm brings $\sigma_t$ into the cache, and if $|C_{t-1}| = k$ it first evicts one page $q \in C_{t-1}$, so $C_t = C_{t-1} \setminus \{q\} \cup \{\sigma_t\}$. On a hit it keeps $C_t = C_{t-1}$. The *fault rate* is $A(\sigma)/n$, and the *hit ratio* is $1 - A(\sigma)/n$.

Faults are often split into three kinds (the [three Cs model](/three-cs-model/)):

- a **compulsory** or cold fault is the first request for a page; every algorithm has it if the cache starts empty;
- a **capacity** fault is a fault, other than a compulsory one, that a fully associative cache of the same size and with the same policy would also have;
- a **conflict** fault comes from a restricted placement, as in a [set-associative cache](/set-associative-cache/); it does not exist in the fully associative model of the paging problem.

## Examples and non-examples

Take $k = 2$, an empty cache and $\sigma = a\,b\,a\,c\,b$ with [LRU](/lru/) replacement.

| $t$ | $\sigma_t$ | cache before | fault? | evicted | cache after |
|---|---|---|---|---|---|
| 1 | $a$ | $\{\}$ | yes (cold) | | $\{a\}$ |
| 2 | $b$ | $\{a\}$ | yes (cold) | | $\{a, b\}$ |
| 3 | $a$ | $\{a, b\}$ | no, a hit | | $\{a, b\}$ |
| 4 | $c$ | $\{a, b\}$ | yes (cold) | $b$ | $\{a, c\}$ |
| 5 | $b$ | $\{a, c\}$ | yes | $a$ | $\{b, c\}$ |

So $\mathrm{LRU}(\sigma) = 4$. The fault at $t = 5$ is not forced: an algorithm that evicts $a$ at $t = 4$ has a hit at $t = 5$ and 3 faults in total, which is optimal because there are 3 distinct pages.

**Non-examples.**

- A request for a page that is in the cache is a hit, even if the page was loaded long ago or is about to be evicted.
- An eviction is not a fault. A rule such as [flush when full](/flush-when-full/) evicts $k$ pages on one fault, and it pays 1 for that fault.
- A *prefetch*, a load of a page that is not requested now, is not a fault in this definition, but in the general model it costs 1 as a load. The [demand paging](/demand-paging/) theorem shows that prefetching never lowers the number of loads in this model.

## Related definitions

- [Paging problem](/paging-problem/): the problem that counts faults, with its offline and online versions.
- [Demand paging](/demand-paging/): bring in a page only on a fault.
- [Cache hit ratio](/cache-hit-ratio/): the fraction of requests that are hits.
- [Miss ratio curve](/miss-ratio-curve/): the fault rate as a function of the cache size $k$, computed in one pass for [stack algorithms](/stack-algorithms/).
- [Belady's algorithm](/belady-algorithm/): the offline rule with the fewest faults.
- [Weighted paging](/weighted-paging-problem/): each fault on page $p$ costs a weight $w(p)$ instead of 1.

## References
