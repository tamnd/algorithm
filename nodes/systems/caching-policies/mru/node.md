---
tag: TH6NND
kind: algorithm
slug: mru
name: Most recently used (MRU)
aliases:
- MRU
- Most recently used (MRU) replacement
- most recently used replacement
area: systems/caching-policies
level: intro
summary: On a miss with a full cache, evict the most recently used page. Optimal on cyclic scans larger than the cache, but not competitive.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [lru, paging-problem]
see_also: [lru, belady-optimal, lru-cache, random-replacement, lru-k, cache-replacement-policy]
sources:
  - paper: "Hong-Tai Chou and David J. DeWitt, An evaluation of buffer management strategies for relational database systems, Proceedings of the 11th International Conference on Very Large Data Bases (VLDB), 1985, 127-141"
    locator: the query locality set model and the looping sequential reference pattern, served with MRU
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 22, Beyond Physical Memory, Policies (the looping sequential workload, and MRU and MFU as the opposites of LRU and LFU)
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the optimal offline rule MIN, used here as the reference
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1 (LIFO and the paging rules that are not competitive)
---

Most recently used (MRU) is the [cache replacement policy](/cache-replacement-policy/) that, on a miss with a full cache, evicts the page whose last request is the most recent one. It is the mirror image of [LRU](/lru/). On a cyclic scan over more pages than the cache holds, MRU makes exactly the choices of the offline optimum [MIN](/belady-optimal/), while LRU misses on every request. On other workloads it can be very bad: it is not competitive for the [paging problem](/paging-problem/).

## In plain words

Picture a reading list that you go through again and again, in the same order, and a shelf that holds all the books but one. LRU sends back the book you read longest ago, and that is exactly the next book on the list, so every book must be fetched. MRU does the opposite: it sends back the book you just finished. That book is the one you need last in the next round, so most of the shelf stays useful.

MRU is a good rule only when a page you just used is the one you will need again latest. That is true for a loop. It is false for most programs, which reuse recent data soon. Then MRU throws away the most useful page.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ pages of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. MRU is online and deterministic.

## The algorithm

MRU keeps the cached pages in recency order, the least recently used first, as LRU does. Only the end of the eviction differs.

```pseudo id=main
MRU-ACCESS(p)                    ▷ cache C in recency order, capacity k
L1  if p ∈ C then
L2      move p to the most recent end of C
L3      return hit
L4  if |C| = k then
L5      remove the most recent page of C        ▷ the eviction
L6  put p at the most recent end of C
L7  return miss
```

The page evicted at line L5 is the page requested last before $p$. So MRU only needs the identity of the last requested page, not a full order: after line L6, the most recent page is $p$. The structure of the [LRU cache](/lru-cache/) with the eviction at the other end of the list also works in $O(1)$ time.

## Example

Run MRU with $k = 3$ on three rounds of the loop $0, 1, 2, 3$. The cache is listed from the least to the most recently used.

| $t$ | request | result | evicted | cache after |
| --- | --- | --- | --- | --- |
| 1 to 3 | 0, 1, 2 | 3 misses | | 0 1 2 |
| 4 | 3 | miss | 2 | 0 1 3 |
| 5 | 0 | hit | | 1 3 0 |
| 6 | 1 | hit | | 3 0 1 |
| 7 | 2 | miss | 1 | 3 0 2 |
| 8 | 3 | hit | | 0 2 3 |
| 9 | 0 | hit | | 2 3 0 |
| 10 | 1 | miss | 0 | 2 3 1 |
| 11 | 2 | hit | | 3 1 2 |
| 12 | 3 | hit | | 1 2 3 |

MRU has 6 misses on the 12 requests. LRU has 12 misses: it misses on every request of this loop. After the first round, MRU misses once in each $k = 3$ requests. In general, on $n$ requests of the loop $0, 1, \ldots, k$, MRU has exactly $(k + 1) + \lfloor (n - k - 1)/k \rfloor$ misses for $n \ge k + 1$, which is the same count as MIN.

**A bad case.** Request $1, 2, \ldots, k$ and then $k + 1, k, k + 1, k, \ldots$. At the request of $k + 1$, MRU evicts $k$; at the next request of $k$, it evicts $k + 1$; and so on. Each request is a miss, while MIN evicts page 1 once and then hits on every request.

## Correctness

MRU serves each request and keeps at most $k$ pages, by the same argument as for LRU: the list $C$ holds the cached pages in the order of their last requests, a hit only moves $p$ to the recent end, and a miss with a full cache removes one page before adding $p$.

**Optimality on loops.** Let $\sigma$ be a cyclic trace, $\sigma_t = t \bmod L$ for $t = 0, 1, \ldots, n - 1$, with $L > k$. At a miss with a full cache at time $t$, each cached page $q$ was last requested at some time $\ell_q < t$, and its next request is at $\ell_q + L$, because the trace repeats with period $L$. So the order of the next requests of the cached pages is the order of their last requests. The most recently used page has the largest $\ell_q$, so its next request is the furthest in the future. This is exactly the page that MIN evicts, and the times $\ell_q$ are distinct, so there is no tie. MRU and MIN start from the same empty cache and make the same eviction at each miss, so they have the same misses. By [Belady's theorem](/belady-optimal/), MIN has the fewest misses of all policies, so MRU is optimal on $\sigma$. The full proof is below.

The same argument shows more: MRU is optimal on each trace where, at each miss, the cached page with the latest last request also has the latest next request.

## Complexity

- **Time.** $O(1)$ expected time per request with a hash set and a recency list, so $O(n)$ expected time in total.
- **Space.** $\Theta(k)$.
- **Misses.** On a loop of $L > k$ pages, MRU has the optimal number of misses. In the worst case it has no competitive ratio: on the bad case above, MRU has $n$ misses and MIN has $k + 1$, for each length $n$. So no bound $\mathrm{MRU}(\sigma) \le \alpha \cdot \mathrm{MIN}(\sigma) + \beta$ holds with constants $\alpha$ and $\beta$.

## Properties

- **Not competitive.** By the bad case. The rule LIFO, which evicts the page that entered the cache last, fails on the same kind of trace; MRU and LIFO differ because a hit changes the MRU order and not the LIFO order.
- **Not a marking algorithm.** For $k \ge 2$, at the second request of $k$ in the bad case, MRU evicts page $k + 1$, which was requested in the current $k$-phase. So MRU is not a [marking algorithm](/marking-algorithm/).
- **A stack algorithm.** MRU ranks the cached pages by a priority (the time of the last request) that does not depend on the cache size, so the cache of size $k$ is inside the cache of size $k + 1$ at each step, and MRU has no [Belady anomaly](/belady-anomaly/). See the [inclusion property](/inclusion-property/).
- **Fixed pages.** Pages that are not requested again stay forever, because MRU never evicts a page that is older than the newest one.

## Variants and improvements

- **MRU for one access pattern.** Database buffer managers do not use MRU for everything. The query locality set model of Chou and DeWitt gives each file access its own buffer pool and its own rule, and uses MRU for the looping sequential pattern of a nested loop join.
- **Random replacement.** [Random replacement](/random-replacement/) also avoids the zero hit ratio of LRU on loops, without knowledge of the pattern, at a cost on other traces.
- **Scan-resistant policies.** [2Q](/two-q/), [LRU-K](/lru-k/) and [ARC](/arc/) detect pages that are used only once in a scan and keep them out of the main area, which helps scans that do not repeat.

## When to use it

Use MRU only when you know the access pattern is a repeated sequential scan of a file or a table that is larger than its buffer, for example the inner relation of a [nested loop join](/nested-loop-join/). Give that scan its own buffer, and use LRU or a scan-resistant rule for the rest. Do not use MRU as the general policy of a cache.

## Pitfalls

- **MRU as a general policy.** On workloads with temporal locality it evicts the page that is most likely to be used next.
- **MRU and LIFO.** They are different rules. LIFO evicts the last loaded page; MRU evicts the last used page.
- **Cold pages that never leave.** Pages loaded once and never used again fill the cache over time.
- **The loop length.** MRU wins only when the loop is longer than the cache. If the loop fits, every policy hits after the first round.

## Implementations

## History

The opposite rules MRU and MFU appear in operating system texts as counterexamples to LRU and LFU, and they do poorly on most programs. MRU found its use in database buffer management. Chou and DeWitt (1985) classified the reference patterns of relational queries and used MRU for the looping sequential pattern in their DBMIN buffer manager. The optimality on a pure loop follows from Belady's theorem on the offline optimum.

## References
