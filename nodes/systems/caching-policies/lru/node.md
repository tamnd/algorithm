---
tag: C24R9P
kind: algorithm
slug: lru
name: Least recently used (LRU)
aliases:
- LRU
- LRU replacement
- Least recently used (LRU) replacement
- least recently used
- LRU page replacement
area: systems/caching-policies
level: intro
summary: On a miss with a full cache, evict the page whose last request is the oldest. A stack algorithm and k-competitive.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1970
  people: [Richard L. Mattson, Jan Gecsei, Donald R. Slutz, Irving L. Traiger]
  note: LRU was in use in virtual memory systems in the 1960s. Mattson, Gecsei, Slutz and Traiger showed in 1970 that it is a stack algorithm, and Sleator and Tarjan proved in 1985 that it is k-competitive.
prereqs: [paging-problem, cache-replacement-policy]
see_also: [lru-cache, fifo-replacement, clock, lru-k, mru, belady-optimal, lru-competitiveness, inclusion-property]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging part of the paper, LRU and FIFO with k pages against MIN with h pages
  - paper: doi:10.1147/sj.92.0078
    title: "Richard L. Mattson, Jan Gecsei, Donald R. Slutz and Irving L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the definition of stack algorithms, with LRU as the main example
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 10, Section 10.4.4 (LRU page replacement) and Section 10.4.5 (LRU-approximation page replacement)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 22, Beyond Physical Memory, Policies (the sections on LRU, the looping workload and approximating LRU)
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1 (LRU as a marking algorithm) and Section 3.2 (the bound k/(k-h+1))
---

Least recently used (LRU) is the [cache replacement policy](/cache-replacement-policy/) that, on a miss with a full cache, evicts the page whose most recent request is the oldest. It is the default policy of many operating systems, databases and libraries, and it serves each request in $O(1)$ time with the [LRU cache](/lru-cache/) structure. It is a stack algorithm, so a larger cache never has more misses, and it is $k$-competitive for the [paging problem](/paging-problem/). It does badly on a loop over more pages than fit in the cache, where it misses on every request.

## In plain words

You have a small shelf for a few books and a large library behind you. When you need a book that is on the shelf, you take it, and you put it back on the shelf. When you need a book that is not on the shelf and the shelf is full, you must send one book back to the library first. LRU sends back the book that you used least recently, the one that has stayed untouched the longest.

The bet is that the recent past predicts the near future. A book you used a minute ago is likely to be used again soon, and a book that has sat for an hour is not. This is often true for programs. When the bet is wrong, as in a loop over slightly too many books, LRU does very badly.

## The problem

The model is the [paging problem](/paging-problem/). A cache holds at most $k$ pages, all of the same size. A request sequence $\sigma = \sigma_1 \sigma_2 \ldots \sigma_n$ names one page at each step. If the page is in the cache, the request is a hit. If not, it is a miss: the page is loaded, and if the cache is full, one cached page is evicted first. The cost is the number of misses. The policy is online: it decides each eviction without knowledge of later requests. The cache starts empty.

## The algorithm

The policy keeps the cached pages in recency order, the least recently used first.

```pseudo id=main
LRU-ACCESS(p)                    ▷ cache C in recency order, capacity k
L1  if p ∈ C then
L2      move p to the most recent end of C
L3      return hit
L4  if |C| = k then
L5      remove the least recent page of C       ▷ the eviction
L6  put p at the most recent end of C
L7  return miss
```

The rule is the same as "evict the page with the smallest time of last request". The recency order is only a way to find that page fast. With a [hash table](/hash-table/) from page to node and a [doubly linked list](/doubly-linked-list/) in recency order, lines L1 to L6 each take $O(1)$ time. The [LRU cache](/lru-cache/) page gives this structure in full. This page is about the policy: which page goes, and how many misses that gives.

## Example

Run LRU with $k = 3$ on the reference string $\sigma = 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1$ of Silberschatz, Galvin and Gagne. The cache column lists the pages from the least to the most recently used.

| $t$ | request | result | evicted | cache after |
| --- | --- | --- | --- | --- |
| 1 | 7 | miss | | 7 |
| 2 | 0 | miss | | 7 0 |
| 3 | 1 | miss | | 7 0 1 |
| 4 | 2 | miss | 7 | 0 1 2 |
| 5 | 0 | hit | | 1 2 0 |
| 6 | 3 | miss | 1 | 2 0 3 |
| 7 | 0 | hit | | 2 3 0 |
| 8 | 4 | miss | 2 | 3 0 4 |
| 9 | 2 | miss | 3 | 0 4 2 |
| 10 | 3 | miss | 0 | 4 2 3 |
| 11 | 0 | miss | 4 | 2 3 0 |
| 12 | 3 | hit | | 2 0 3 |
| 13 | 2 | hit | | 0 3 2 |
| 14 | 1 | miss | 0 | 3 2 1 |
| 15 | 2 | hit | | 3 1 2 |
| 16 | 0 | miss | 3 | 1 2 0 |
| 17 | 1 | hit | | 2 0 1 |
| 18 | 7 | miss | 2 | 0 1 7 |
| 19 | 0 | hit | | 1 7 0 |
| 20 | 1 | hit | | 7 0 1 |

LRU has 12 misses and 8 hits. On the same string, [FIFO](/fifo-replacement/) has 15 misses and the offline optimum [MIN](/belady-optimal/) has 9. At $t = 6$, LRU evicts 1 and keeps 2, because 2 was requested at $t = 4$ and 1 at $t = 3$; MIN evicts 1 there too. The two first differ at $t = 8$: LRU evicts 2, the least recently used page, while MIN evicts 0, whose next request at $t = 11$ is the latest, so MIN hits at $t = 9$ and $t = 10$.

**The loop.** Request the pages $0, 1, \ldots, k$ in a cycle. Each requested page is the one page of the cycle that is not among the last $k$ distinct pages, so LRU misses on every request. MIN misses about once in $k$ requests on the same trace, and [MRU](/mru/) does as well as MIN there.

## Correctness

The invariant of LRU-ACCESS is: after request $t$, the cache holds exactly the $\min(k, d_t)$ distinct pages that were requested most recently, where $d_t$ is the number of distinct pages in $\sigma_1 \ldots \sigma_t$, and $C$ lists them in the order of their last requests. A hit moves $p$ to the recent end, which restores the order. A miss with a full cache removes the page whose last request is the oldest of the $k$, and that page is the one that drops out of the $k$ most recent distinct pages when $p$ joins them. So the evicted page is always the least recently used one, as the rule says. The full proof is below.

A direct consequence: request $\sigma_t$ is a hit if and only if fewer than $k$ distinct other pages were requested since the last request of $\sigma_t$. That number is the [reuse distance](/reuse-distance/) of the request. So LRU hits exactly the requests with reuse distance less than $k$.

## Complexity

- **Time.** With the hash map and the doubly linked list of the [LRU cache](/lru-cache/), each request takes $O(1)$ time: worst case for the list work, expected for the hash lookup. A run over $n$ requests takes $O(n)$ expected time. With a search over $k$ time stamps instead, a miss costs $O(k)$.
- **Space.** $\Theta(k)$: one list node and one map entry for each cached page.
- **Misses, worst case.** A deterministic online policy can be made to miss on each request, by requesting always the page that it does not hold. The loop of $k + 1$ pages does this for LRU.
- **Misses against the optimum.** For each $\sigma$, $\mathrm{LRU}_k(\sigma) \le \frac{k}{k - h + 1}\,\mathrm{MIN}_h(\sigma) + c$, with a constant $c$ that does not depend on $\sigma$, when MIN has $h \le k$ pages. With $h = k$ this is the $k$-competitive bound, and no deterministic online policy has a ratio less than $k$. The statement and the proof are on [LRU competitiveness](/lru-competitiveness/). With both caches empty at the start, $\mathrm{LRU}_k(\sigma) \le k \cdot \mathrm{MIN}_k(\sigma)$ holds with no additive term.

## Properties

- **A stack algorithm.** By the invariant, the LRU cache of size $k$ is the set of the $k$ most recent distinct pages, which is a subset of the LRU cache of size $k + 1$ at every step. This is the [inclusion property](/inclusion-property/). So the number of misses never rises when $k$ grows, and LRU has no [Belady anomaly](/belady-anomaly/). The [Mattson stack algorithm](/mattson-stack-algorithm/) uses this to get the misses of all sizes in one pass.
- **A marking algorithm.** LRU never evicts a page that was requested in the current $k$-phase, so it is a [marking algorithm](/marking-algorithm/), and the $k$ bound also follows from that class.
- **Recency only.** LRU does not count requests. A page requested once a minute ago beats a page requested a thousand times an hour ago. One long scan of new pages flushes the whole cache.
- **Deterministic and online.** The eviction depends only on the past requests.

## Variants and improvements

- **CLOCK.** [CLOCK](/clock/) keeps one reference bit for each page instead of a full order. It costs less on each hit, which matters when hardware sets the bit, and it behaves close to LRU.
- **LRU-K.** [LRU-K](/lru-k/) ranks pages by the time of their $K$-th most recent request. It resists scans, at a higher cost for each miss.
- **2Q and SLRU.** [2Q](/two-q/) and [SLRU](/slru/) keep new pages in a separate area, so that a page must be requested twice before it can push out the hot pages.
- **ARC and LIRS.** [ARC](/arc/) adapts the split between recency and frequency, and [LIRS](/lirs/) ranks pages by reuse distance. Both use [ghost lists](/ghost-lists/) of evicted pages.
- **Pseudo-LRU in hardware.** Set-associative caches use [tree pseudo-LRU](/plru-replacement/) with $k - 1$ bits per set.

## When to use it

Use LRU as the default policy when the workload has temporal locality and no long scans, and when an $O(1)$ cost per request and a simple proof of behavior matter. Use it when you need the [miss ratio curve](/miss-ratio-curve/) for all sizes, because the stack property gives it in one pass. Do not use plain LRU for a buffer pool that serves large scans, or for a loop over more data than the cache. Use a scan-resistant policy there, such as [2Q](/two-q/), [ARC](/arc/) or [LRU-K](/lru-k/), or [MRU](/mru/) for a pure loop.

## Pitfalls

- **Updating the order only on a miss.** That is [FIFO](/fifo-replacement/), not LRU. A hit must move the page to the recent end.
- **Counting the first $k$ misses.** With an empty cache, the first request to each page is a miss for every policy. Compare policies on the same start state.
- **The loop of $k + 1$ pages.** A cyclic access to a little more data than the cache gives a hit ratio of zero. A larger cache, by one page, gives a hit ratio close to one.
- **A global lock.** In a concurrent program, each hit writes to the shared list. This makes LRU slow under many threads, which is a main reason for CLOCK and sampled LRU in practice.
- **LRU is not MIN.** LRU looks at the past and MIN at the future. They agree only on some traces.

## Implementations

## History

Replacement by recency was in use in the virtual memory systems of the 1960s. Belady compared replacement rules by simulation in 1966, with the offline optimum MIN as the reference. Mattson, Gecsei, Slutz and Traiger defined stack algorithms in 1970 and showed that LRU is one, which gave the one-pass method to measure all cache sizes. Sleator and Tarjan proved in 1985 that LRU and FIFO with $k$ pages miss at most $k/(k - h + 1)$ times as often as MIN with $h$ pages, and that no deterministic online rule does better.

## References
