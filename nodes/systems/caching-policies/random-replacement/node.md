---
tag: TVHW25
kind: algorithm
slug: random-replacement
name: Random replacement
aliases:
- RAND
- random eviction
- RANDOM paging algorithm
area: systems/caching-policies
level: intro
summary: On a miss with a full cache, evict a page chosen uniformly at random. Memoryless, k-competitive in expectation, and no zero hit ratio on loops.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1989
  people: [Prabhakar Raghavan, Marc Snir]
  note: Random replacement was in use in early virtual memory and cache designs. Raghavan and Snir proved in 1989 that it is k-competitive against an adaptive online adversary.
prereqs: [paging-problem, randomized-online-algorithm]
see_also: [lru, fifo-replacement, randomized-marking, oblivious-adversary, adaptive-adversary, harmonic-paging-bound, mru, belady-optimal]
sources:
  - paper: "Prabhakar Raghavan and Marc Snir, Memory versus randomization in on-line algorithms, Proceedings of ICALP 1989, LNCS 372, Springer, 687-703"
    title: Memory versus randomization in on-line algorithms
    locator: the algorithm RANDOM for paging and its bound k against an adaptive online adversary
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 4 (randomized paging, the algorithm RAND and its competitive ratio)
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B, Section B.1 (block replacement, random against LRU and FIFO)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 22, Beyond Physical Memory, Policies (the random policy and the looping sequential workload)
---

Random replacement (RAND) is the [cache replacement policy](/cache-replacement-policy/) that, on a miss with a full cache, evicts a cached page chosen uniformly at random. It keeps no history at all, so a hit costs nothing and the state is just the set of cached pages. On a loop over $k + 1$ pages, where [LRU](/lru/) and [FIFO](/fifo-replacement/) miss on every request, it misses on about $2/(k + 1)$ of the requests. Raghavan and Snir proved that it is $k$-competitive in expectation for the [paging problem](/paging-problem/), even against an [adaptive adversary](/adaptive-adversary/).

## In plain words

When a full shelf needs room for one more book, you close your eyes and take out any book, each with the same chance. You do not keep any notes about which book you used when.

This sounds careless, and on many workloads it is somewhat worse than LRU. But it has no blind spot that a fixed pattern can always hit. A loop that is a little longer than the shelf makes LRU and FIFO throw out exactly the book needed next, every time. A random choice throws out that book only now and then. And because there is nothing to update on a hit, the rule is cheap to build in hardware.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ pages of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. RAND is online and randomized: the cost on a fixed $\sigma$ is a random variable, and we bound its expectation. Against an [oblivious adversary](/oblivious-adversary/), $\sigma$ is fixed in advance. Against an adaptive online adversary, each request may depend on the past random choices.

## The algorithm

```pseudo id=main
RANDOM-ACCESS(p)                 ▷ set C of cached pages, capacity k
L1  if p ∈ C then return hit
L2  if |C| = k then
L3      choose q uniformly at random from C
L4      remove q from C
L5  add p to C
L6  return miss
```

The implementation keeps the cached pages in an array of $k$ slots and a hash map from page to slot. Line L3 draws a uniform slot. Line L4 moves the last page of the array into the hole, so that the array has no gaps. The random generator is a parameter, so that a run can be repeated with a fixed seed.

## Example

**The loop of $k + 1$ pages.** Request $0, 1, \ldots, k$ in a cycle. The first $k + 1$ requests are misses. From then on, the cache holds $k$ of the $k + 1$ pages. At a miss at time $t$, the page evicted is uniform among the $k$ cached pages, and these pages are requested next at times $t + 1, t + 2, \ldots, t + k$, one each. So the next miss comes after $D$ requests, with $D$ uniform on $\{1, \ldots, k\}$ and independent of the past. The mean gap is $(k + 1)/2$, so in the long run RAND misses on a fraction $2/(k + 1)$ of the requests.

| policy, $k = 3$, 30 rounds of $0, 1, 2, 3$ ($n = 120$) | misses |
| --- | --- |
| LRU, FIFO | 120 |
| RAND, exact expectation | 61.83 |
| MRU and MIN | 42 |

The expectation $61.83$ is $4 + 57.83$: four cold misses, then close to $\frac{2}{4} \cdot 116 = 58$. MIN and [MRU](/mru/) miss once in each $k$ requests after the first round. So on the loop, RAND is between the worst and the best possible.

**A short run.** With $k = 3$ and the trace $0, 1, 2, 3, 0, 1, 2, 3$, the first eviction is at the request of 3, and each of 0, 1 and 2 is evicted with probability $1/3$. If 2 goes, the next requests 0 and 1 hit; if 0 goes, the next request is a miss at once. The exact law of the number of misses on a short trace follows from a walk over all cache states with these probabilities, and the test code checks the simulation against it.

## Correctness

After each request, the requested page is cached and $|C| \le k$: a hit changes nothing, and a miss with a full cache removes one page before it adds one. The array with the swap of the last page keeps exactly the cached pages, each at the slot that the hash map names. Line L3 draws each of the $k$ slots with probability $1/k$, and each slot holds a different page, so each cached page is evicted with probability $1/k$. The full proof, with the loop rate, is below.

## Complexity

- **Time.** $O(1)$ expected time per request: one hash lookup, one random number on a miss, and a constant number of array writes. So $O(n)$ expected in total. A hit writes nothing.
- **Space.** $\Theta(k)$ for the array and the map. There is no per-page history.
- **Against the optimum.** For each $\sigma$, $\mathbb{E}[\mathrm{RAND}_k(\sigma)] \le k \cdot \mathrm{OPT}_k(\sigma) + c$ for a constant $c$, against an adaptive online adversary (Raghavan and Snir 1989). An oblivious adversary is weaker, so the same bound holds against it. This is the same ratio $k$ as LRU and FIFO, and it is far above the ratio $2H_k$ of [randomized marking](/randomized-marking/), where $H_k = 1 + 1/2 + \cdots + 1/k$. No randomized policy beats $H_k$ against an oblivious adversary; see the [harmonic paging bound](/harmonic-paging-bound/).
- **The loop.** A long-run miss rate of $2/(k + 1)$ on the loop of $k + 1$ pages, against 1 for LRU and FIFO and about $1/k$ for MIN.

## Properties

- **Memoryless.** The state is only the set of cached pages. Raghavan and Snir used RAND to show that randomization can stand in for memory: a policy with no history matches the best deterministic ratio $k$.
- **No fixed worst case.** A single fixed trace cannot force a miss on each request with probability 1 once the trace repeats pages, as the loop shows. A deterministic policy always has such a trace.
- **Not a marking algorithm.** RAND can evict a page that was requested a moment ago.
- **Not a stack algorithm in the usual sense.** Two runs with different sizes make independent choices, so the cache of size $k$ need not be inside the cache of size $k + 1$.

## Variants and improvements

- **Randomized marking.** [Randomized marking](/randomized-marking/) evicts a random page among the pages not yet requested in the current phase. This one change brings the ratio from $k$ down to $2H_k$ against an oblivious adversary.
- **Sampled LRU.** Draw a few cached pages at random and evict the least recently used of them. Redis approximates LRU in this way, with a sample of a few keys.
- **Pseudo-random replacement in hardware.** Caches with many ways use a linear feedback shift register in place of true random numbers. See [set-associative cache](/set-associative-cache/).

## When to use it

Use random replacement in hardware caches with high associativity, where LRU state per set costs too much and a hit must not write state. Use it as a baseline in experiments, or when the workload may contain loops a little larger than the cache. Prefer LRU or a scan-resistant policy when the workload has strong temporal locality, because RAND throws out hot pages as often as cold ones.

## Pitfalls

- **The global random state.** Tests and simulations need a generator with a fixed seed, passed in as a parameter, so that a run can be repeated.
- **A biased choice.** Picking a slot with a modulo of a short random number, or removing from a list in a way that leaves gaps, can make some pages more likely to go. Check that each page goes with probability $1/k$.
- **Including the new page.** The victim is drawn from the $k$ cached pages before the new page is added. Drawing from $k + 1$ pages, the new one included, is a different rule.
- **Reading one run as the expectation.** A single seeded run varies. Report the mean over many seeds, or compute the expectation exactly on small cases.

## Implementations

## History

Random replacement was among the rules that Belady compared by simulation in 1966, and processor caches have used random or pseudo-random replacement since then because it needs no state per block. Raghavan and Snir studied it in the competitive model in 1989, in a paper on memory versus randomization: they proved that RAND is $k$-competitive against an adaptive online adversary.

## References
