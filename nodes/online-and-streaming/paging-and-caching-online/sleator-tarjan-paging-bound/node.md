---
tag: EWT67X
kind: theorem
slug: sleator-tarjan-paging-bound
name: Sleator and Tarjan paging bound
aliases:
- k-competitiveness of LRU
- Sleator-Tarjan paging bound
- (h,k)-paging bound
- resource augmentation bound for paging
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: LRU is k-competitive for paging, and every deterministic online paging algorithm has competitive ratio at least k.
prereqs: [marking-phases, online-caching-lower-bound, lru]
see_also: [lru-competitiveness, fifo-replacement, marking-algorithm, flush-when-full, cache-replacement-policy, harmonic-paging-bound, competitive-ratio, list-update-problem]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging theorems, LRU and FIFO with cache k against MIN with cache h, and the matching lower bound for every on-line rule
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.2, the (h,k)-paging problem, and the k-competitiveness of LRU and FIFO
  - paper: "Neal E. Young, The k-server dual and loose competitiveness for paging, Algorithmica 11(6) (1994), 525-541"
    title: The k-server dual and loose competitiveness for paging
    locator: the bound k/(k-h+1) for marking and conservative algorithms, and loose competitiveness
---

The Sleator and Tarjan paging bound says that LRU and FIFO with a cache of $k$ pages have at most $k/(k - h + 1)$ times as many [faults](/page-fault/) as an optimal offline algorithm with a cache of $h \le k$ pages, plus a constant, and that no deterministic online algorithm does better. With $h = k$ this is the classical statement: LRU and FIFO are $k$-competitive, and $k$ is the best ratio of a deterministic rule. Sleator and Tarjan proved it in 1985, in the paper that started competitive analysis. The bound holds for every [marking algorithm](/marking-algorithm/) and every conservative algorithm, and it shows how much a larger cache helps: with twice the cache of the optimum, LRU is 2-competitive.

## Statement

Use the [paging problem](/paging-problem/) model with cost 1 per page loaded. For $1 \le h \le k$, let $\mathrm{OPT}_h(\sigma)$ be the least cost of an offline algorithm with a cache of $h$ pages, and let the online algorithm have a cache of $k$ pages. The initial caches are arbitrary.

A paging algorithm is *conservative* if it has at most $k$ faults on each contiguous part of $\sigma$ that requests at most $k$ distinct pages. LRU, FIFO and CLOCK are conservative, see [cache replacement policy](/cache-replacement-policy/).

**Theorem.** Let $1 \le h \le k$.

1. **Upper bound.** If $A$ is a marking algorithm or a conservative algorithm with cache size $k$, then for every request sequence $\sigma$,
$$A(\sigma) \le \frac{k}{k - h + 1} \, \mathrm{OPT}_h(\sigma) + k.$$
In particular LRU and FIFO are $k$-competitive ($h = k$).
2. **Lower bound.** Let $A$ be a deterministic online algorithm with cache size $k$. For each $n \ge 1$ there is a sequence $\sigma$ of $n$ requests over $k + 1$ pages with
$$A(\sigma) \ge n \quad\text{and}\quad \mathrm{OPT}_h(\sigma) \le \frac{k - h + 1}{k}(n - 1) + h.$$
So if $A(\sigma) \le c \cdot \mathrm{OPT}_h(\sigma) + b$ for all $\sigma$, then $c \ge k/(k - h + 1)$. With $h = k$: no deterministic online paging algorithm is better than $k$-competitive.

## In plain words

Cut the requests into rounds, each with as many different pages as the cache holds. A rule like least recently used misses at most once per page in a round. So it misses at most as many times per round as the cache has slots.

The best rule that sees the future may have a smaller cache. Across each round and the first request of the next one, it must see one more page than the online cache holds, and it can hold only its own number of pages. So it misses at least the difference plus one times per round.

The ratio of these two counts is the bound. An adversary can force it: it always asks for the one page that the online rule does not hold, and a smart rule with the smaller cache misses only that often.

## Proof

The full proof is in [proofs/main.md](proofs/main.md). The upper bound uses the [phases](/marking-phases/) of $\sigma$: each phase is a maximal part with $k$ distinct pages, so $A$ has at most $k$ faults per phase, and the window from the second request of a phase to the first request of the next one has $k$ distinct pages other than the page just served, which forces $\mathrm{OPT}_h$ to load at least $k - h + 1$ of them. The lower bound uses the adversary of the [deterministic lower bound](/online-caching-lower-bound/) on $k + 1$ pages, and an averaging argument over $\binom{k}{h-1}$ offline algorithms with cache $h$, of which exactly a fraction $(k - h + 1)/k$ fault at each request.

## Consequences

- **LRU, FIFO and FWF have ratio exactly $k$.** The upper bound applies to them, and the lower bound applies to every deterministic rule. So among deterministic rules they are optimal, together with every [marking algorithm](/marking-algorithm/) such as [flush when full](/flush-when-full/). See also [LRU competitiveness](/lru-competitiveness/).
- **Resource augmentation.** With $k = 2h$, the ratio is $2h/(h + 1) < 2$. A modest increase of the online cache brings the ratio to a constant, which explains why LRU does well in practice even though its worst-case ratio is $k$.
- **Some rules are not covered.** LFU and MRU are neither marking nor conservative, and they are not competitive at all. The two classes differ: FWF is marking but not conservative, and FIFO is conservative but not marking.
- **Randomized rules.** Against an [oblivious adversary](/oblivious-adversary/), the lower bound $k$ fails. [Randomized marking](/randomized-marking/) is $2H_k$-competitive, and $H_k$ is optimal ([harmonic bound](/harmonic-paging-bound/)). With a smaller optimal cache, $h < k$, the best randomized ratio is of order $\log(k/(k - h))$ (Young 1991).
- **List update.** The same paper proves that [move to front](/move-to-front/) is 2-competitive for the [list update problem](/list-update-problem/), with the potential function method.

## Tightness

Both parts match: the upper bound and the lower bound have the same ratio $k/(k - h + 1)$ for every $h$. Take $k = 4$, the cycle $0\,1\,2\,3\,4\,0\,1\,\ldots$ of $n = 24$ requests over 5 pages, and empty initial caches. This is the sequence that the adversary builds against LRU.

| $h$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $\mathrm{LRU}_4(\sigma)$ | 24 | 24 | 24 | 24 |
| $\mathrm{OPT}_h(\sigma)$ | 24 | 19 | 14 | 9 |
| bound $\frac{k - h + 1}{k}(n - 1) + h$ | 24 | 19.25 | 14.5 | 9.75 |
| ratio $\mathrm{LRU}_4/\mathrm{OPT}_h$ | 1 | 1.26 | 1.71 | 2.67 |
| $k/(k - h + 1)$ | 1 | 1.33 | 2 | 4 |

The ratio tends to $k/(k - h + 1)$ as $n$ grows, so no smaller factor is possible for LRU, and by part 2 none is possible for any deterministic rule.

## History

Sleator and Tarjan (1985) proved that LRU and FIFO with cache $k$ have at most about $k/(k - h + 1)$ times the faults of MIN with cache $h$, and that no on-line rule has a better ratio. The term *competitive* came a few years later, from Karlin, Manasse, Rudolph and Sleator (1988). Young (1994) extended the bound to all marking and conservative algorithms and introduced loose competitiveness, a form of the bound that holds for most cache sizes at once.

## References
