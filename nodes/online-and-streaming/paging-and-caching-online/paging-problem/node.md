---
tag: PD2CF4
kind: problem
slug: paging-problem
name: Paging problem
aliases:
- Cache replacement problem
- caching problem
- page replacement
- page replacement problem
- paging problem
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Serve a sequence of page requests with a cache of k pages, minimizing faults by choosing evictions.
prereqs: [online-algorithm, competitive-ratio]
see_also: [belady-algorithm, cache-replacement-policy, marking-algorithm, randomized-marking, sleator-tarjan-paging-bound, harmonic-paging-bound, k-server-problem, weighted-paging-problem]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging part of the paper (LRU and FIFO against MIN, the lower bound for on-line rules, and the comparison with a smaller cache)
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Paging, deterministic algorithms (Sections 3.1 to 3.4), and Chapter 4, Paging, randomized algorithms
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the replacement algorithms studied and the optimal offline rule MIN
  - paper: doi:10.1007/BFb0029564
    title: "Sandy Irani, Competitive analysis of paging, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: the survey chapter on deterministic and randomized paging
---

The paging problem asks how to serve a sequence of requests for pages with a fast memory, the *cache*, that holds at most $k$ pages, so that the number of [page faults](/page-fault/) is as small as possible. When a requested page is not in a full cache, the algorithm must choose a page to evict. The offline version, where the whole sequence is known, is solved exactly by [Belady's algorithm](/belady-algorithm/). The online version is the first problem of [competitive analysis](/competitive-ratio/): deterministic algorithms such as [LRU](/lru/) are $k$-competitive and no deterministic algorithm does better, and randomized algorithms reach $H_k \approx \ln k$ against an [oblivious adversary](/oblivious-adversary/).

## In plain words

A computer has a small fast memory and a large slow memory. Programs ask for pages of data one at a time. If the page is in the fast memory, the request is free. If it is not, the page must come from the slow memory, which is expensive. This is a fault. When the fast memory is full, some page must leave to make room.

The question is which page to throw out. If you know all future requests, throw out the page that is needed again last. In real systems you do not know the future, so you need a rule that uses only the past. The theory compares such rules with the best choice made with full knowledge of the future.

## Definition

Notation, used on all the paging pages:

| Symbol | Meaning |
|---|---|
| $\sigma = \sigma_1 \sigma_2 \cdots \sigma_n$ | the request sequence, each $\sigma_t$ a page |
| $n$ | the length of $\sigma$ |
| $k$ | the cache size, $k \ge 1$ |
| $C_t$ | the set of pages in the cache after request $t$ is served |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the number of faults of the algorithm and of an optimal offline algorithm on $\sigma$ |
| $c$ | the competitive ratio |

**The model.** There is a set of pages, finite or infinite. The cache holds a set $C$ of pages with $|C| \le k$. Unless a page says otherwise, the cache starts empty, $C_0 = \emptyset$. Request $t$ names a page $\sigma_t$. Before it is served, the algorithm may change its cache, and after the change $\sigma_t \in C_t$ must hold. The cost is the number of pages that are brought into the cache. In a *demand paging* algorithm, the cache changes only when $\sigma_t \notin C_{t-1}$: then the algorithm brings in $\sigma_t$, and if $|C_{t-1}| = k$ it evicts exactly one page. Such a request is a [page fault](/page-fault/), and the cost is the number of faults. [Demand paging](/demand-paging/) loses nothing: each algorithm can be turned into a demand paging algorithm with at most the same cost on every sequence. So we count faults.

**Offline paging.** Input: $k$ and the whole sequence $\sigma$. Output: a sequence of evictions with the least number of faults, $\mathrm{OPT}(\sigma)$.

**Online paging.** The algorithm learns $\sigma_t$ only at request $t$, and it must choose its eviction before it sees $\sigma_{t+1}$. A deterministic online algorithm $\mathrm{ALG}$ is *$c$-competitive* if there is a constant $b$, independent of $\sigma$, such that

$$\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b \quad \text{for every } \sigma.$$

It is *strictly* $c$-competitive if this holds with $b = 0$. A randomized online algorithm is $c$-competitive against an oblivious adversary if $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$, where the expectation is over the random choices of the algorithm and $\sigma$ is fixed in advance. The [adaptive adversaries](/adaptive-adversary/) of Ben-David, Borodin, Karp, Tardos and Wigderson choose $\sigma_t$ after they see the earlier random choices. The [competitive ratio](/competitive-ratio/) of an algorithm is the infimum of the $c$ for which it is $c$-competitive.

## Variants

- **$(h, k)$-paging.** The online algorithm has a cache of $k$ pages and the offline optimum only $h \le k$. This is resource augmentation. The best deterministic ratio is $k/(k - h + 1)$, see the [Sleator and Tarjan bound](/sleator-tarjan-paging-bound/).
- **Weighted paging.** Each page has a cost to bring in. See the [weighted paging problem](/weighted-paging-problem/). It is the $k$-server problem on a star.
- **File caching or generalized caching.** Pages have sizes and costs. The [Landlord algorithm](/landlord-algorithm/) is $k$-competitive for it.
- **The $k$-server problem.** Paging is the [$k$-server problem](/k-server-problem/) on a uniform metric, where each move costs 1.
- **Paging with predictions.** The algorithm gets a guess of the next request time of each page. See [learning-augmented marking](/learning-augmented-marking/).
- **Locality models.** Access graphs and the [working set model](/working-set-model/) restrict the sequences to model [locality of reference](/locality-of-reference/).
- **Write costs.** Evicting a changed page costs a write. See the [write-back policy](/write-back-policy/).

## Examples

Take $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$ with an empty start. The table gives the number of faults.

| algorithm | $k = 3$ | $k = 4$ |
|---|---|---|
| OPT ([Belady](/belady-algorithm/)) | 7 | 6 |
| [LRU](/lru/) | 10 | 8 |
| [FIFO](/fifo-replacement/) | 9 | 10 |
| [flush when full](/flush-when-full/) | 12 | 10 |

Each algorithm has at least 5 faults, one for each distinct page, so these first faults are forced. FIFO has more faults with the larger cache. This is [Belady's anomaly](/belady-anomaly/), see [stack algorithms](/stack-algorithms/).

**A hard sequence.** With $k = 3$ and the cycle $1\,2\,3\,4\,1\,2\,3\,4\,1\,2\,3\,4$, LRU and FIFO fault on all 12 requests. OPT has 6 faults: 4 first faults and then one fault each 3 requests. This is the idea of the [deterministic lower bound](/online-caching-lower-bound/).

## Known algorithms

- [Belady's algorithm](/belady-algorithm/) (MIN, LFD): offline, evicts the page whose next request is furthest in the future. It is optimal ([Belady's optimality theorem](/belady-optimality/)) and runs in $O(n \log n)$ time.
- [LRU](/lru/) and [FIFO](/fifo-replacement/): online, deterministic, $k$-competitive (Sleator and Tarjan 1985).
- [Marking algorithms](/marking-algorithm/), with LRU and [flush when full](/flush-when-full/) as members: all are $k$-competitive.
- [Randomized marking](/randomized-marking/): $2H_k$-competitive against an oblivious adversary (Fiat et al. 1991), and exactly $2H_k - 1$ (Achlioptas, Chrobak and Noga 2000).
- Partition (McGeoch and Sleator 1991) and Equitable (Achlioptas, Chrobak and Noga 2000): $H_k$-competitive against an oblivious adversary, which is optimal.
- [Random replacement](/random-replacement/): $k$-competitive against an adaptive online adversary (Raghavan and Snir).
- The [cache replacement policy](/cache-replacement-policy/) page compares LRU, FIFO, LFU, CLOCK, MRU and random.

## Bounds

| setting | upper bound | lower bound |
|---|---|---|
| offline | OPT is computed exactly in $O(n \log n)$ time | none needed |
| deterministic online | $k$ (LRU, FIFO, any marking algorithm) | $k$ ([proof](/online-caching-lower-bound/)) |
| deterministic, $(h, k)$ | $k/(k - h + 1)$ (LRU, FIFO) | $k/(k - h + 1)$ ([proof](/sleator-tarjan-paging-bound/)) |
| randomized, oblivious adversary | $H_k$ (Partition, Equitable) | $H_k$ ([proof](/harmonic-paging-bound/)) |
| randomized, adaptive offline adversary | $k$ | $k$, since randomization does not help against this adversary (Ben-David et al. 1994) |

Here $H_k = 1 + 1/2 + \cdots + 1/k$ is the $k$-th [harmonic number](/harmonic-series/), with $\ln(k+1) < H_k \le 1 + \ln k$.

## Reductions

- Paging with cache size $k$ is the [$k$-server problem](/k-server-problem/) on the uniform metric over the set of pages: a server on a point is a page in the cache. So each $k$-server bound gives a paging bound, and each paging lower bound is a $k$-server lower bound.
- Paging is a special case of [metrical task systems](/metrical-task-systems/), with one state for each possible cache.
- A paging algorithm can be turned into a [demand paging](/demand-paging/) algorithm with no more faults on any sequence. The new algorithm simulates the old one and stays online.

## Applications

Virtual memory in operating systems, CPU caches, database buffer pools, web and content delivery caches, and the block transfers of the [external memory model](/external-memory-model/) are all paging problems. Real systems use [LRU](/lru/), [CLOCK](/clock/), [ARC](/arc/), [2Q](/two-q-replacement/) and others. The theory explains why LRU-like rules are robust, and Belady's algorithm gives the lower bound that a trace-driven study compares with.

## References
