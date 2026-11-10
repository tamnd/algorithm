---
tag: QC5DH4
kind: theorem
slug: online-caching-lower-bound
name: Lower bound for deterministic online caching
aliases:
- deterministic paging lower bound
- lower bound k for paging
area: online-and-streaming/paging-and-caching-online
level: core
summary: Shows that no deterministic online caching algorithm can have a competitive ratio better than the cache size k.
prereqs: [paging-problem, belady-algorithm, adversary-argument, competitive-ratio]
see_also: [harmonic-paging-bound, sleator-tarjan-paging-bound, marking-algorithm, lru, adaptive-offline-adversary, k-server-problem, k-server-conjecture, randomized-marking]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the theorem that no on-line paging rule is better than k-competitive against MIN, and its form with a smaller optimal cache
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, the lower bound k for deterministic paging algorithms
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gábor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the theorem that randomization gives no gain against an adaptive offline adversary
  - paper: "Mark S. Manasse, Lyle A. McGeoch and Daniel D. Sleator, Competitive algorithms for server problems, Journal of Algorithms 11(2) (1990), 208-230"
    title: Competitive algorithms for server problems
    locator: the lower bound k for the k-server problem on each metric space with more than k points
---

The lower bound for deterministic online caching says that for each cache size $k$, no deterministic online paging algorithm is $c$-competitive with $c < k$. The proof is an [adversary argument](/adversary-argument/) on $k + 1$ pages: the adversary always requests the one page that the algorithm does not hold, so the algorithm faults on every request, while [Belady's algorithm](/belady-algorithm/) faults at most once in every $k$ requests. Sleator and Tarjan proved it in 1985. Since LRU, FIFO and every [marking algorithm](/marking-algorithm/) are $k$-competitive, the bound is tight, and randomized algorithms beat it only because the adversary cannot see their cache, as the [harmonic bound](/harmonic-paging-bound/) shows.

## Statement

Use the [paging problem](/paging-problem/) model: a cache of $k$ pages, a cost of 1 for each page loaded, and $\mathrm{OPT}(\sigma)$ the least cost of an offline algorithm with the same initial cache.

**Theorem.** Let $k \ge 1$ and let $A$ be a deterministic online paging algorithm with cache size $k$. Suppose that there are constants $c$ and $b$ with $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every request sequence $\sigma$. Then $c \ge k$.

More exactly: for each $n \ge 1$ there is a sequence $\sigma$ of $n$ requests over $k + 1$ pages with $A(\sigma) \ge n$ and $\mathrm{OPT}(\sigma) \le 1 + \lfloor (n - 1)/k \rfloor$, when both start with the same full cache. The result also holds with an empty initial cache, and for each set of more than $k$ pages.

## In plain words

Take one page more than the cache holds. Whatever the cache holds, one page is missing. An adversary who knows the rule can always tell which page is missing, and asks for exactly that page. So the rule misses on every request.

A rule that sees the future does much better on the same requests. When it must throw out a page, it picks the one asked for last among those it holds. All the other pages it holds are asked for before that page comes back, so it gets at least as many hits in a row as the cache has slots, less one. So it misses at most once in each stretch of requests as long as the cache size. The ratio between the two is the cache size.

## Proof

**The adversary.** Fix $k$ and $A$, and let the pages be $1, \ldots, k + 1$. Both $A$ and the offline algorithm start with the cache $C_0 = \{1, \ldots, k\}$. For $t = 1, \ldots, n$, let $\sigma_t$ be a page not in the cache of $A$ after request $t - 1$; one exists, because that cache has at most $k$ of the $k + 1$ pages. Since $A$ is deterministic and online, its cache after request $t - 1$ depends only on $\sigma_1, \ldots, \sigma_{t-1}$, so this defines $\sigma$. At each request, $A$ must load $\sigma_t$, so $A(\sigma) \ge n$. Also $\sigma_{t+1} \ne \sigma_t$, because $\sigma_t$ is in the cache of $A$ after request $t$.

**The offline algorithm.** Let LFD be Belady's rule on $\sigma$ with the start $C_0$: on a fault, evict the cached page whose next request is furthest in the future. We show that two faults of LFD are at least $k$ requests apart.

Let LFD fault at time $t$. Before the request its cache holds $k$ of the $k + 1$ pages and not $\sigma_t$, so it holds all pages other than $\sigma_t$. It evicts the page $q$ with the furthest next request, and after request $t$ it holds all pages other than $q$. If $q$ is never requested again, LFD never faults again. Otherwise, let $s$ be the next request for $q$. Every request in $t + 1, \ldots, s - 1$ is for a page other than $q$, so it is a hit, and the next fault is at $s$. The $k - 1$ cached pages other than $q$ and $\sigma_t$ each have a next request before $s$, by the choice of $q$. These are $k - 1$ distinct times in $t + 1, \ldots, s - 1$, so $s \ge t + k$.

So the faults of LFD are at times $t_1 < t_2 < \cdots$ with $t_{j+1} - t_j \ge k$ and $t_1 \ge 1$. In $n$ requests there are at most $1 + \lfloor (n - 1)/k \rfloor$ of them. By [Belady's optimality theorem](/belady-optimality/), $\mathrm{OPT}(\sigma) = \mathrm{LFD}(\sigma) \le 1 + (n - 1)/k$.

**The ratio.** If $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, then for every $n$,

$$n \le c \left(1 + \frac{n - 1}{k}\right) + b.$$

Divide by $n$ and let $n \to \infty$: $1 \le c/k$, so $c \ge k$.

**An empty start.** If both caches start empty, use the same adversary. LFD has at most $k$ faults before its cache is full. After that, at each fault its cache holds all pages other than $\sigma_t$, and the argument above applies without change. So $\mathrm{OPT}(\sigma) \le k + 1 + (n - 1)/k$, and the limit is the same. With more than $k + 1$ pages, the adversary uses only $k + 1$ of them. $\blacksquare$

## Consequences

- **LRU and FIFO are optimal deterministic rules.** They are $k$-competitive ([Sleator and Tarjan bound](/sleator-tarjan-paging-bound/)), so their competitive ratio is exactly $k$, and so is the ratio of every deterministic [marking algorithm](/marking-algorithm/) and of [flush when full](/flush-when-full/).
- **The $k$-server problem.** Paging is the [$k$-server problem](/k-server-problem/) on a uniform metric. Manasse, McGeoch and Sleator (1990) extended the argument to every metric space with more than $k$ points, so no deterministic $k$-server algorithm is better than $k$-competitive. The [$k$-server conjecture](/k-server-conjecture/) states that $k$ is reached on every metric.
- **Randomization against weak adversaries.** The proof needs the adversary to know the cache of the algorithm. A randomized algorithm hides its cache from an [oblivious adversary](/oblivious-adversary/), and [randomized marking](/randomized-marking/) is $2H_k$-competitive. The best randomized ratio is $H_k$, by the [harmonic bound](/harmonic-paging-bound/). So $k$ and $H_k \approx \ln k$ are the deterministic and the randomized answers to the same question.
- **Randomization against strong adversaries.** Against an [adaptive offline adversary](/adaptive-offline-adversary/), which sees the random choices, Ben-David, Borodin, Karp, Tardos and Wigderson (1994) proved that randomization gives no gain. So the bound $k$ holds for randomized paging algorithms against that adversary too.
- **A smaller optimal cache.** If OPT has only $h \le k$ pages, the same idea gives the lower bound $k/(k - h + 1)$, see the [Sleator and Tarjan bound](/sleator-tarjan-paging-bound/).

## Tightness

The bound is exact. Take $k = 3$, the initial cache $\{1, 2, 3\}$ with 1 loaded first and used least recently, and LRU or FIFO. The adversary requests the missing page each time, which gives the cycle $4\,1\,2\,3\,4\,1\,2\,3\,4\,1\,2\,3$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\sigma_t$ | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 |
| LRU | F | F | F | F | F | F | F | F | F | F | F | F |
| LFD | F, evict 3 | | | F, evict 2 | | | F, evict 1 | | | F, evict 4 | | |

LRU has 12 faults and LFD has 4, which is $1 + \lfloor 11/3 \rfloor$. The ratio is $3 = k$. Since LRU is $k$-competitive, the bound $c \ge k$ cannot be raised. The additive constant $b$ plays no role: the gap grows linearly with $n$. The bound needs only $k + 1$ distinct pages. With exactly $k$ pages, every algorithm has at most $k$ faults, so a universe of more than $k$ pages is necessary.

## History

Sleator and Tarjan (1985) proved in the same paper that LRU and FIFO are $k$-competitive against MIN and that no on-line rule is better, with the comparison against an optimum with a smaller cache. Manasse, McGeoch and Sleator (1990) generalized the lower bound to the $k$-server problem. Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) showed that randomization reduces the ratio to $\Theta(\log k)$ against an oblivious adversary, and Ben-David, Borodin, Karp, Tardos and Wigderson (1994) showed that it does not help against an adaptive offline adversary.

## References
