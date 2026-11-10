---
tag: 5WP5GD
kind: algorithm
slug: marking-algorithm
name: Marking algorithm
aliases:
- deterministic marking
- marking algorithms
- MARK class
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Evicts only unmarked pages within each phase; k-competitive and generalizes LRU and FWF.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {worst: O(n k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1991
  people: [Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator, Neal E. Young]
  note: Fiat, Karp, Luby, McGeoch, Sleator and Young defined marking algorithms and k-phases in their paper on competitive paging, and showed that each one is k-competitive.
prereqs: [marking-phases, paging-problem, competitive-ratio]
see_also: [flush-when-full, randomized-marking, lru, cache-replacement-policy, learning-augmented-marking, online-caching-lower-bound, sleator-tarjan-paging-bound]
sources:
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the definition of marking algorithms and the bound k for each of them
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1, marking algorithms and the theorem that each one is k-competitive
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the bound k for LRU, a marking algorithm
  - paper: doi:10.1007/BFb0029564
    title: "Sandy Irani, Competitive analysis of paging, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: the section on marking algorithms
---

A marking algorithm is an online paging rule that marks each page when it is requested, unmarks all pages when a request finds all cached pages marked, and never evicts a marked page. Which unmarked page to evict is left open, so the name covers a class of rules: [LRU](/lru/) and [flush when full](/flush-when-full/) are members, and [randomized marking](/randomized-marking/) picks the page at random. Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) showed that each member is $k$-competitive, by a phase argument. Since no deterministic online rule is better than $k$-competitive, each deterministic member is optimal in this measure.

## In plain words

Each page in the cache has a flag. When a page is used, raise its flag. When room is needed, throw out a page without a flag. If all pages have flags and a new page is needed, lower all flags first.

Why is this a good rule? A flag means "used in this round". A round ends when the cache has been filled with pages that were all used in it. Inside a round, a page that was used stays, so each different page can miss only once. Even a rule that sees the future must miss at least once for each round, so the marking rule is at most as many times worse as the cache has slots.

## The problem

The input is a cache size $k \ge 1$ and a sequence $\sigma = \sigma_1 \cdots \sigma_n$ of page requests, given one at a time. The cache starts empty. On each fault with a full cache, the algorithm must evict one page before it sees the next request. The goal is a small number of faults compared with $\mathrm{OPT}(\sigma)$, the number of faults of [Belady's algorithm](/belady-algorithm/), in the sense of the [competitive ratio](/competitive-ratio/).

## The algorithm

The set $C$ is the cache and $M \subseteq C$ is the set of marked pages. The parameter CHOOSE is any rule that returns a page of a non-empty set. It may use the past requests.

```pseudo id=main
MARKING(σ, k, CHOOSE)                           ▷ σ = σ_1 .. σ_n, cache size k ≥ 1
L1  C ← ∅, M ← ∅, faults ← 0
L2  for t ← 1 to n do
L3      p ← σ_t
L4      if p ∉ C then
L5          faults ← faults + 1
L6          if |C| = k then
L7              if M = C then M ← ∅            ▷ all cached pages marked: a new phase
L8              q ← CHOOSE(C \ M)              ▷ any unmarked page
L9              C ← C \ {q}
L10         C ← C ∪ {p}
L11     M ← M ∪ {p}
L12 return faults
```

A wider definition calls an algorithm a marking algorithm if it never evicts a marked page, with the marks as above. This includes [flush when full](/flush-when-full/), which evicts all unmarked pages at line L7 at once. The pseudocode is the [demand paging](/demand-paging/) form, with one eviction per fault.

**Members.**

- CHOOSE = the unmarked page whose last request is oldest gives [LRU](/lru/). A marked page was requested in the current phase, after each unmarked page, so the page that LRU evicts is always unmarked.
- CHOOSE = a uniform random unmarked page gives [randomized marking](/randomized-marking/).
- CHOOSE = an unmarked page that a predictor expects to be requested last gives [learning-augmented marking](/learning-augmented-marking/).
- FIFO and CLOCK are not members: they can evict a page that was requested in the current phase (see [cache replacement policy](/cache-replacement-policy/)).

## Example

Take $k = 3$, $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$, and CHOOSE = the oldest unmarked page, which is LRU. The [phases](/marking-phases/) are $[1\,2\,3]$, $[4\,1\,2]$, $[5\,1\,2]$ and $[3\,4\,5]$.

| $t$ | $\sigma_t$ | result | new phase | evicted | marked after | unmarked after |
|---|---|---|---|---|---|---|
| 1 | 1 | fault | phase 1 | | 1 | |
| 2 | 2 | fault | | | 1, 2 | |
| 3 | 3 | fault | | | 1, 2, 3 | |
| 4 | 4 | fault | phase 2 | 1 | 4 | 2, 3 |
| 5 | 1 | fault | | 2 | 4, 1 | 3 |
| 6 | 2 | fault | | 3 | 4, 1, 2 | |
| 7 | 5 | fault | phase 3 | 4 | 5 | 1, 2 |
| 8 | 1 | hit | | | 5, 1 | 2 |
| 9 | 2 | hit | | | 5, 1, 2 | |
| 10 | 3 | fault | phase 4 | 5 | 3 | 1, 2 |
| 11 | 4 | fault | | 1 | 3, 4 | 2 |
| 12 | 5 | fault | | 2 | 3, 4, 5 | |

There are 10 faults in 4 phases, at most $k = 3$ in each phase. With CHOOSE = the unmarked page whose last request is newest, the same sequence has 8 faults. OPT has 7, and the phase bound gives $\mathrm{OPT} \ge 4$.

## Correctness

The schedule is valid: at line L8 the set $C \setminus M$ is not empty. Indeed $M \subseteq C$ always holds, because a page enters $M$ only at line L11 when it is in $C$, and line L9 evicts only a page outside $M$. So if $M \ne C$, then $C \setminus M \ne \emptyset$, and if $M = C$, line L7 empties $M$ and $C \setminus M = C$ has $k \ge 1$ pages. The invariant is: after request $t$, $M$ is the set of distinct pages requested so far in the current [phase](/marking-phases/). Line L7 runs exactly when the request is a page outside the $k$ distinct pages of the current phase, which is when a new phase starts. Since marked pages are never evicted, each distinct page of a phase faults at most once in the phase, so $\mathrm{ALG}(\sigma) \le kN$ for $N$ phases. Each algorithm has at least $N$ faults with an empty start, so $\mathrm{ALG}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$.

## Complexity

- **Per request.** Keep $C$ and $M$ as two hash maps, each ordered by last request, as in the [LRU cache](/lru-cache/). A hit costs $O(1)$ expected time. On a fault with a full cache, line L7 swaps the two maps in $O(1)$ time, because when $M = C$ all cached pages move from marked to unmarked at once.
- **The rule.** In the implementation, CHOOSE gets the unmarked pages as a list, which costs $O(k)$ per eviction, so the time is $O(nk)$ in the worst case. A fixed rule that reads the map directly, such as the oldest unmarked page or a random one from an array with swap removal, costs $O(1)$ per request, so $O(n)$ expected time in total.
- **Space.** $O(k)$ for the cache and the marks.

## Properties

- **$k$-competitive.** $\mathrm{ALG}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$ with an empty start, and $\mathrm{ALG}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k$ with a common initial cache, for each CHOOSE.
- **Optimal among deterministic rules.** No deterministic online rule is better than $k$-competitive ([lower bound](/online-caching-lower-bound/)). On the cycle of $k + 1$ pages, LRU faults on every request.
- **Resource augmentation.** Against an optimum with a cache of $h \le k$ pages, each marking algorithm is $k/(k - h + 1)$-competitive, the best possible ([Sleator and Tarjan bound](/sleator-tarjan-paging-bound/)).
- **Online and demand paging.** The pseudocode reads only past requests and evicts only on a fault with a full cache.
- **Not every $k$-competitive rule is marking.** FIFO is $k$-competitive and not marking. Its bound comes from the wider class of conservative rules.
- **Phases are fixed.** The phases depend only on $\sigma$ and $k$, so all members agree on when a phase starts and on the marked set.

## Variants and improvements

- **Randomized marking.** A uniform random choice at line L8 gives $2H_k - 1$ against an [oblivious adversary](/oblivious-adversary/) ([randomized marking](/randomized-marking/)), much better than $k$ for large $k$. Chrobak, Koutsoupias and Noga (2003) showed that marking algorithms, random or not, cannot reach a ratio much below $2H_k$.
- **Partition and Equitable.** To reach the optimal randomized ratio $H_k$, these rules may evict a page that was requested in the current phase, so they are not marking algorithms (see the [harmonic bound](/harmonic-paging-bound/)).
- **Predictions.** [Learning-augmented marking](/learning-augmented-marking/) picks by predicted next request, and keeps a bound of $O(\log k)$ when the predictions are bad.
- **Weighted pages.** The marking idea does not carry over to costs; [weighted paging](/weighted-paging-problem/) and the [Landlord algorithm](/landlord-algorithm/) use credits instead.

## When to use it

Use the marking framework to design or analyse a paging rule. To prove that a new rule is $k$-competitive, it is enough to show that it never evicts a page requested in the current phase. In a real cache, choose the member by the expected pattern: LRU for recency, a random choice when an adversary may know the rule, or a prediction when one is available. FWF is mostly a teaching example.

## Pitfalls

- **Resetting the marks too early.** Line L7 must run only on a fault with a full cache whose pages are all marked. Resetting on each fault, or on a hit, breaks the link with the phases and the bound.
- **Marking only on a fault.** Line L11 must mark the page on a hit too. If hits do not mark, the rule can evict a page used in the current phase, and the bound $k$ is lost.
- **Calling FIFO a marking algorithm.** FIFO is $k$-competitive, but it can evict a marked page. The marking proof does not cover it.
- **Comparing with OPT on a different start.** The strict bound $k \cdot \mathrm{OPT}$ needs an empty start. With a common non-empty start, add $k$.

## Implementations

## History

Sleator and Tarjan (1985) proved that LRU and FIFO are $k$-competitive and that $k$ is the best ratio for deterministic rules. Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) defined the $k$-phases and the class of marking algorithms, proved that each member is $k$-competitive, and analysed the random member. Borodin and El-Yaniv (1998) present the marking class as the main tool for deterministic paging.

## References
