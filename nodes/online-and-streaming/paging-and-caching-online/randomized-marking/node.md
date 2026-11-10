---
tag: 6JHBAR
kind: algorithm
slug: randomized-marking
name: Randomized marking
aliases:
- random marking
- MARK
- the randomized marking algorithm
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Evicts a random unmarked page; achieves 2H_k competitive ratio against an oblivious adversary.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {expected: O(n)}
  space: {extra: O(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1991
  people: [Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator, Neal E. Young]
  note: Fiat, Karp, Luby, McGeoch, Sleator and Young introduced the algorithm MARK and proved that it is 2H_k-competitive against an oblivious adversary, and that no randomized algorithm is better than H_k-competitive.
prereqs: [marking-algorithm, oblivious-adversary, harmonic-series, randomized-online-algorithm]
see_also: [harmonic-paging-bound, marking-phases, flush-when-full, random-replacement, learning-augmented-marking, adaptive-adversary, linearity-of-expectation]
sources:
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the algorithm MARK, the proof of the bound 2H_k with new and stale pages, and the lower bound H_k
  - paper: doi:10.1016/S0304-3975(98)00116-9
    title: "Dimitris Achlioptas, Marek Chrobak and John Noga, Competitive analysis of randomized paging algorithms, Theoretical Computer Science 234(1-2) (2000), 203-218"
    locator: the exact competitive ratio 2H_k - 1 of MARK, and the algorithm Equitable
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 4, the randomized marking algorithm MARK and its analysis
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 13, Online algorithms, the randomized marking algorithm for paging
---

Randomized marking (MARK) is the [marking algorithm](/marking-algorithm/) that, on a [fault](/page-fault/) with a full cache, evicts a page chosen uniformly at random among the unmarked cached pages. Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) proved that it is $2H_k$-competitive against an [oblivious adversary](/oblivious-adversary/), where $H_k = 1 + 1/2 + \cdots + 1/k \approx \ln k$, an exponential gain over the deterministic bound $k$. Achlioptas, Chrobak and Noga (2000) showed that its exact ratio is $2H_k - 1$. The best possible ratio for randomized paging is $H_k$ ([harmonic bound](/harmonic-paging-bound/)), so MARK is within a factor of 2 of optimal.

## In plain words

Use the flag rule of the marking algorithms: raise a page's flag when it is used, lower all flags when all cached pages have flags and a new page is needed, and never throw out a page with a flag. Among the pages without a flag, pick the one to throw out at random.

Why does chance help? A deterministic rule can be fooled: an adversary who knows the rule always asks for the page it just threw out. With a random choice, the adversary does not know which page is gone. When it asks for an old page, the page is often still there. The loss of the online rule then grows only like the logarithm of the cache size, not like the cache size.

## The problem

The input is a cache size $k \ge 1$ and a sequence $\sigma = \sigma_1 \cdots \sigma_n$ of page requests, given one at a time, with an empty cache at the start. A randomized online algorithm may use random bits. It is *$c$-competitive against an oblivious adversary* if there is a constant $b$ with $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$. The sequence is fixed before the random choices, and the expectation is over those choices only ([randomized online algorithm](/randomized-online-algorithm/)).

## The algorithm

The set $C$ is the cache, and the array $U$ holds the unmarked cached pages, so $C \setminus U$ is the set of marked pages.

```pseudo id=main
RANDOMIZED-MARKING(σ, k)                        ▷ σ = σ_1 .. σ_n, cache size k ≥ 1
L1  C ← ∅, U ← an empty array, faults ← 0
L2  for t ← 1 to n do
L3      p ← σ_t
L4      if p ∉ C then
L5          faults ← faults + 1
L6          if |C| = k then
L7              if U is empty then U ← the pages of C          ▷ all marked: a new phase, unmark all
L8              q ← a uniform random element of U
L9              remove q from U and from C
L10         C ← C ∪ {p}                                        ▷ p is marked: it is not in U
L11     else if p ∈ U then remove p from U                     ▷ mark p
L12 return faults
```

To remove an element from $U$ in $O(1)$ time, keep a map from each page in $U$ to its index, move the last element of $U$ into the hole, and update its index.

## Example

Take $k = 3$ and $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3$. The [phases](/marking-phases/) are $[1\,2\,3]$, $[4\,1\,2]$, $[5\,1\,2]$ and $[3]$. A page of a phase is *new* if it is not in the phase before, and *stale* otherwise. The column $\Pr$ gives the exact probability of a fault.

| $t$ | $\sigma_t$ | page type | why | $\Pr[\text{fault}]$ |
|---|---|---|---|---|
| 1 to 3 | 1, 2, 3 | new | empty cache | 1 each |
| 4 | 4 | new | a random page of {1, 2, 3} is evicted | 1 |
| 5 | 1 | stale | 1 is the evicted page with probability 1/3 | 1/3 |
| 6 | 2 | stale | one of 2 and 3 is missing, each with the same chance | 1/2 |
| 7 | 5 | new | a random unmarked page is evicted | 1 |
| 8 | 1 | stale | one of the 3 stale pages is missing | 1/3 |
| 9 | 2 | stale | one of the 2 unrequested stale pages is missing | 1/2 |
| 10 | 3 | new | 3 is not in phase 3 | 1 |

The expected number of faults is $3 + \frac{11}{6} + \frac{11}{6} + 1 = \frac{23}{3} \approx 7.67$. OPT has 6 faults. A deterministic marking algorithm can have up to 10 faults here, as [flush when full](/flush-when-full/) does.

## Correctness

Each run is a run of a [marking algorithm](/marking-algorithm/): $U$ is always the set of unmarked cached pages, and line L8 picks from $U$. So each run is a valid demand paging schedule with at most $k$ faults per phase, whatever the random choices are.

For the bound $2H_k$, let phase $i$ have $m_i$ new pages, with $m_1$ the number of distinct pages of phase 1. Each new page faults once. When the $j$-th distinct stale page is first requested in phase $i$, the unrequested stale pages are $k - j + 1$ pages, and exactly $\ell \le m_i$ of them are missing, where $\ell$ is the number of new pages requested so far. By symmetry, the missing set is a uniform random set of size $\ell$, so the probability of a fault is $\ell/(k - j + 1) \le m_i/(k - j + 1)$. Summing, the expected faults in phase $i$ are at most $m_i(1 + H_k - H_{m_i}) \le m_i H_k$. The new pages of two consecutive phases force $\mathrm{OPT}(\sigma) \ge \frac{1}{2}\sum_i m_i$. So $\mathbb{E}[\mathrm{MARK}(\sigma)] \le 2H_k \cdot \mathrm{OPT}(\sigma)$.

## Complexity

- **Per request.** A hit costs $O(1)$ expected time for the hash lookups, and a removal from $U$ costs $O(1)$ with the swap. A fault costs $O(1)$ expected time plus one random index.
- **Phase start.** Line L7 copies the $k$ cached pages into $U$, at a cost of $O(k)$. It runs once per phase, and each phase except the last has at least $k$ requests, so this is $O(1)$ amortized per request.
- **Total.** $O(n)$ expected time and $O(k)$ space. The random bits are $O(\log k)$ per fault.

## Properties

- **$2H_k$-competitive against an oblivious adversary**, with $b = 0$ from an empty start. The exact ratio is $2H_k - 1$ (Achlioptas, Chrobak and Noga 2000). For $k = 2, 3, 4$ this is $2$, $8/3$ and $19/6$.
- **$k$-competitive on every run.** Every run is a marking algorithm, so the bound $k$ holds for every outcome of the random choices, also against [adaptive adversaries](/adaptive-adversary/).
- **Within a factor 2 of optimal.** No randomized algorithm is better than $H_k$-competitive against an oblivious adversary ([harmonic bound](/harmonic-paging-bound/)).
- **Tight for each phase.** If each phase requests its $m$ new pages first and then its stale pages, the expected faults of the phase are exactly $m(1 + H_k - H_m)$.
- **Online and demand paging.** It reads only past requests and evicts one page only on a fault with a full cache.

## Variants and improvements

- **Partition and Equitable.** McGeoch and Sleator (1991) gave the algorithm Partition, and Achlioptas, Chrobak and Noga (2000) the simpler Equitable. Both are $H_k$-competitive, which is optimal. They are not marking algorithms.
- **Lower bound for marking.** Chrobak, Koutsoupias and Noga (2003) showed that marking algorithms cannot reach a ratio much below $2H_k$, so the gap to $H_k$ needs rules outside the class.
- **Random replacement.** [RAND](/random-replacement/) evicts a uniform random page from the whole cache. It needs no marks, but its ratio is $k$, not $O(\log k)$.
- **Predictions.** [Learning-augmented marking](/learning-augmented-marking/) evicts the unmarked page with the furthest predicted next request, and falls back to random choices, which keeps an $O(\log k)$ bound with bad predictions.
- **Weighted paging and $k$-server.** Randomized $O(\log k)$-competitive algorithms for [weighted paging](/weighted-paging-problem/) use the [online primal-dual method](/online-primal-dual/) instead of marks.

## When to use it

Use MARK when an adversary may learn a fixed rule and build bad request sequences, for example in a shared cache, or when a simple rule with a guaranteed $O(\log k)$ ratio is needed. It needs one mark bit per page and a random choice per eviction. When access patterns have strong recency, LRU often has fewer faults in practice, and the $O(\log k)$ guarantee holds only in expectation and against an oblivious adversary.

## Pitfalls

- **Choosing among all cached pages.** The random choice must be among the unmarked pages only. A uniform choice among all pages is RAND, with ratio $k$.
- **Forgetting to mark on a hit.** Line L11 must remove a hit page from $U$. Otherwise the algorithm can evict a page used in the current phase, and the analysis fails.
- **An adaptive adversary.** An adversary that sees which page was evicted can always request it, so against it MARK is only $k$-competitive. The $2H_k$ bound needs the sequence to be fixed in advance.
- **Rebuilding $U$ on each fault.** Building $U$ from $C$ costs $O(k)$. It must run only when $U$ is empty, at the start of a phase.
- **Using one random seed for many caches.** In a test or simulation, give each run its own seeded generator, so that runs are independent and the results can be repeated.

## Implementations

## History

Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) introduced MARK, proved that it is $2H_k$-competitive against an oblivious adversary, and proved that no randomized paging algorithm is better than $H_k$-competitive. McGeoch and Sleator (1991) gave the first $H_k$-competitive algorithm, Partition. Achlioptas, Chrobak and Noga (2000) proved that the ratio of MARK is exactly $2H_k - 1$ and gave Equitable, a simpler $H_k$-competitive algorithm.

## References
