---
tag: 9TFRYX
kind: algorithm
slug: flush-when-full
name: Flush-when-full (FWF)
aliases:
- FWF
- flush when full
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Evicts all pages when a fault occurs with a full cache; k-competitive, simple phase-based policy.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {worst: O(n)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1991
  people: [Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator, Neal E. Young]
  note: FWF is the simplest member of the class of marking algorithms that Fiat, Karp, Luby, McGeoch, Sleator and Young defined in 1991, and textbooks use it as the first example of a k-competitive rule.
prereqs: [marking-algorithm]
see_also: [marking-phases, lru, randomized-marking, demand-paging, cache-replacement-policy, online-caching-lower-bound]
sources:
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1, the algorithm FWF and the marking algorithms
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the class of marking algorithms and its bound k
  - paper: doi:10.1007/BFb0029564
    title: "Sandy Irani, Competitive analysis of paging, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: the deterministic algorithms LRU, FIFO and FWF
---

Flush when full (FWF) is the online paging rule that, on a [fault](/page-fault/) with a full cache, evicts all $k$ cached pages and then loads the requested page. Its cache always holds exactly the distinct pages requested so far in the current [phase](/marking-phases/), so it is a [marking algorithm](/marking-algorithm/), and it is $k$-competitive like LRU. It is the worst marking algorithm: on every sequence it has at least as many faults as each other member. It is useful as the simplest example of the phase argument, not as a practical cache.

## In plain words

Fill the cache as pages are asked for. When a new page is needed and the cache is full, empty the whole cache and start again with the new page.

This looks wasteful, and it is: pages that will be needed again are thrown out too. But each round of filling covers as many different pages as the cache holds, and the rule misses once for each of them. A rule that knows the future must also miss at least once in each round. So the simple rule is never worse than the cache size times the best possible.

## The problem

The input is a cache size $k \ge 1$ and a sequence $\sigma = \sigma_1 \cdots \sigma_n$ of page requests, given one at a time, with an empty cache at the start. The algorithm keeps a cache of at most $k$ pages, holds $\sigma_t$ after request $t$, and wants few [page faults](/page-fault/) compared with the offline optimum $\mathrm{OPT}(\sigma)$ of [Belady's algorithm](/belady-algorithm/), in the sense of the [competitive ratio](/competitive-ratio/).

## The algorithm

```pseudo id=main
FWF(σ, k)                                       ▷ σ = σ_1 .. σ_n, cache size k ≥ 1
L1  C ← ∅, faults ← 0
L2  for t ← 1 to n do
L3      p ← σ_t
L4      if p ∉ C then
L5          faults ← faults + 1
L6          if |C| = k then
L7              C ← ∅                           ▷ flush: a new phase starts
L8          C ← C ∪ {p}
L9  return faults
```

In the terms of the marking algorithms, each cached page is marked, and line L7 unmarks and evicts all of them at once. FWF is not a [demand paging](/demand-paging/) rule, since it evicts $k$ pages on one fault.

## Example

Take $k = 3$ and $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3$. The phases are $[1\,2\,3]$, $[4\,1\,2]$, $[5\,1\,2]$ and $[3]$.

| $t$ | $\sigma_t$ | result | flush | cache after |
|---|---|---|---|---|
| 1 | 1 | fault | | {1} |
| 2 | 2 | fault | | {1, 2} |
| 3 | 3 | fault | | {1, 2, 3} |
| 4 | 4 | fault | evicts 1, 2, 3 | {4} |
| 5 | 1 | fault | | {1, 4} |
| 6 | 2 | fault | | {1, 2, 4} |
| 7 | 5 | fault | evicts 1, 2, 4 | {5} |
| 8 | 1 | fault | | {1, 5} |
| 9 | 2 | fault | | {1, 2, 5} |
| 10 | 3 | fault | evicts 1, 2, 5 | {3} |

FWF faults on all 10 requests, which is $3 + 3 + 3 + 1$, the number of distinct pages in each phase. [LRU](/lru/) has 8 faults, because it keeps 1 and 2 at $t = 7$, and OPT has 6.

## Correctness

The invariant is: after request $t$, $C$ is the set of distinct pages requested so far in the current phase. A new phase starts exactly at a request for a page outside the $k$ distinct pages of the current phase, and then $C$ holds those $k$ pages, so line L6 holds and line L7 runs. Inside a phase, $C$ has fewer than $k$ pages or holds the requested page, so line L7 does not run. From the invariant, FWF has exactly one fault for each distinct page of each phase, so $\mathrm{FWF}(\sigma) = \sum_i d_i \le kN$, where $d_i$ is the number of distinct pages of phase $i$ and $N$ is the number of phases. [Marking phases](/marking-phases/) shows $\mathrm{OPT}(\sigma) \ge N$ with an empty start. So $\mathrm{FWF}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$.

## Complexity

- **Time.** Each request does one lookup and at most one insertion in a hash set, $O(1)$ expected time. A flush replaces the set by an empty one. If the old set must be cleared, its $k$ entries were inserted by $k$ loads since the last flush, so the clearing costs $O(1)$ amortized per load. So FWF takes $O(n)$ expected time.
- **Space.** $O(k)$ for the cache.

## Properties

- **$k$-competitive.** $\mathrm{FWF}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$ with an empty start, and the ratio $k$ is reached on the cycle of $k + 1$ pages, where FWF faults on every request. No deterministic rule does better ([lower bound](/online-caching-lower-bound/)).
- **The worst marking algorithm.** Each marking algorithm faults at most once per distinct page per phase, and FWF faults exactly once. So $\mathrm{ALG}(\sigma) \le \mathrm{FWF}(\sigma)$ for each marking algorithm $\mathrm{ALG}$ and each $\sigma$. On $\sigma$ above, FWF has 10 faults and LRU 8.
- **Not demand paging.** Its demand version, built as on the [demand paging](/demand-paging/) page, evicts one unmarked page per fault. It is a marking algorithm with at most as many faults.
- **Not conservative.** With $k = 2$ and $\sigma = 1\,2\,3\,2$, FWF flushes at request 3, so the block $2\,3\,2$, with 2 distinct pages, has 3 faults. FIFO and LRU have at most $k$ faults on such a block.
- **Not a stack algorithm.** With $\sigma = 2\,4\,5\,0$, the cache of size 2 ends as $\{5, 0\}$ and the cache of size 3 as $\{0\}$, so the inclusion property of [stack algorithms](/stack-algorithms/) fails.
- **Resource augmentation.** As a marking algorithm, FWF is $k/(k - h + 1)$-competitive against an optimum with $h \le k$ pages ([Sleator and Tarjan bound](/sleator-tarjan-paging-bound/)).

## Variants and improvements

- **Keep the marked pages.** Evict only one unmarked page per fault instead of all of them. This is the general [marking algorithm](/marking-algorithm/), with LRU as the member that evicts the oldest one.
- **Random choice.** Evict a random unmarked page: [randomized marking](/randomized-marking/) is $2H_k - 1$-competitive against an oblivious adversary.
- **Flush in hardware.** Some translation buffers and software caches clear all entries at once, for example on a change of address space, because a full clear is cheap. FWF models this behaviour.

## When to use it

Use FWF as a teaching example and as a base case in proofs: its cost equals the sum of the distinct pages of the phases, so it is easy to compute and it bounds each marking algorithm from above. In a real cache, a clear on each full fault discards useful pages, and LRU or CLOCK is better at the same guarantee.

## Pitfalls

- **Counting the flush as $k$ faults.** A flush is $k$ evictions and one fault. The cost model counts only the fault.
- **Flushing on each fault.** The flush must run only when the cache is full. Flushing earlier breaks the link with the phases.
- **Assuming FWF is close to LRU.** Let each phase request one new page and then the same $k - 1$ pages. LRU faults about once per phase, and FWF $k$ times per phase. Both are $k$-competitive, but on such sequences FWF has about $k$ times as many faults.
- **Using demand paging results directly.** FWF is not demand paging, so a result stated only for demand paging rules needs the conversion first.

## Implementations

## History

Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) defined the marking algorithms, and FWF is the simplest of them. Borodin and El-Yaniv (1998) and Irani (1998) use FWF, with LRU and FIFO, as a first example of a deterministic $k$-competitive paging rule and as the extreme member of the marking class.

## References
