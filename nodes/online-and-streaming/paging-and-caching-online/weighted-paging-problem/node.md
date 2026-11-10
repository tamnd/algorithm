---
tag: 12SE47
kind: problem
slug: weighted-paging-problem
name: Weighted paging problem
aliases:
- generalized caching problem
- cost-based caching
- weighted caching
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Paging where each page has its own fetch cost, so the goal is to minimize total weighted cost.
prereqs: [paging-problem, competitive-ratio, k-server-problem]
see_also: [landlord-algorithm, greedy-dual, double-coverage, k-server-problem, online-primal-dual, randomized-marking, variable-size-caching, gdsf]
sources:
  - paper: doi:10.1137/0404017
    title: Marek Chrobak, Howard J. Karloff, Tom Payne and Sundar Vishwanathan, New results on server problems, SIAM Journal on Discrete Mathematics 4(2), 1991, 172-181
    locator: the k-competitive deterministic algorithm for weighted caching, as a k-server algorithm on a star, and the offline optimum by minimum-cost flow
  - paper: doi:10.1007/BF01189992
    title: Neal E. Young, The k-server dual and loose competitiveness for paging, Algorithmica 11(6), 1994, 525-541
    locator: the GreedyDual algorithm for weighted caching and its ratio k/(k - h + 1) against an optimum with h slots
  - paper: doi:10.1145/2339123.2339126
    title: Nikhil Bansal, Niv Buchbinder and Joseph Naor, A primal-dual randomized algorithm for weighted paging, Journal of the ACM 59(4), article 19, 2012
    locator: the O(log k)-competitive randomized algorithm, by an online fractional solution and a rounding scheme; the conference version is FOCS 2007
  - paper: "Anna Adamaszek, Artur Czumaj, Matthias Englert and Harald Räcke, An O(log k)-competitive algorithm for generalized caching, Proceedings of SODA 2012"
    locator: the randomized ratio O(log k) for pages of different sizes and costs
  - paper: doi:10.1007/BFb0029564
    title: "Sandy Irani, Competitive analysis of paging, in: Online Algorithms, The State of the Art, Lecture Notes in Computer Science 1442, Springer, 1998"
    locator: the sections on weighted caching and on caching with sizes (the bit, fault and general models)
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 10 (k-server on trees and stars, which covers weighted caching)
---

The weighted paging problem is [paging](/paging-problem/) in which each page $p$ has its own cost $w_p \ge 0$ to load into the cache. An online algorithm must choose which page to evict on each miss, and the aim is a small total cost of the loads, not a small number of misses. Rules that ignore the costs, such as LRU, are not competitive here. The deterministic competitive ratio is still $k$, reached by the rule of Chrobak, Karloff, Payne and Vishwanathan (1991) and by Young's GreedyDual (1994), and the randomized ratio is $\Theta(\log k)$, reached by the algorithm of Bansal, Buchbinder and Naor (2007).

## In plain words

A cache holds $k$ items. Some items are cheap to fetch again, for example from a local disk. Others are expensive, for example from a slow server far away. When the cache is full and a new item arrives, the cache must throw one item out. If it throws out an expensive item that is needed again soon, it pays a lot.

So the cache should prefer to keep expensive items. But it must not keep them for ever: an expensive item that is never used again only wastes a slot. A good rule gives each item a credit equal to its cost, spends the credits of all items over time, and evicts an item when its credit is gone. An item that is used again gets its credit back.

## Definition

**Input.** A cache size $k$, a set of pages with costs $w_p \ge 0$, and a request sequence $\sigma = r_1, \ldots, r_n$. The cache holds at most $k$ pages, and in the usual form it starts empty.

**Rules.** If $r_t$ is in the cache, the request is a hit and costs nothing. Else it is a miss: $r_t$ is loaded for a cost of $w_{r_t}$, and if the cache was full, the algorithm evicts a page of its choice. An online algorithm chooses the page to evict from the requests so far only.

**Cost.** $A(\sigma) = \sum_{\text{misses } t} w_{r_t}$. Some papers charge $w_p$ when $p$ is evicted instead of when it is loaded. The two costs differ by at most the total cost of the $k$ pages in the cache at the end, which is a constant, so the competitive ratios are the same.

**The question.** Find the best competitive ratio $c$, the least $c$ such that some online algorithm has $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, for deterministic and for randomized algorithms.

## Variants

- **Paging.** All costs are $1$. The cost is the number of misses.
- **$k$-server on a star.** Put the pages as leaves of a star, at distance $w_p / 2$ from the center. A lazy server that moves from $q$ to $p$ pays $(w_q + w_p) / 2$, so over a sequence it pays the load cost of the [$k$-server problem](/k-server-problem/) form up to a constant. Weighted paging is the $k$-server problem on a weighted star.
- **Generalized caching.** Each page also has a size $s_p$, and the cache has a total size $k$. This is also called file caching. The special cases are the *bit model* ($w_p = s_p$), the *fault model* ($w_p = 1$), and the *general model* (any $w_p$ and $s_p$). The [Landlord](/landlord-algorithm/) rule handles all of them. The systems view is on the [variable-size caching](/variable-size-caching/) page.
- **Resource augmentation.** The online cache has $k$ slots and the optimum only $h \le k$ slots. GreedyDual is $k / (k - h + 1)$-competitive in this setting.

## Examples

**LRU ignores the costs.** Let $k = 2$, with costs $w_a = w_b = 1$ and $w_c = 10$, and repeat the round $c, a, b$ for $r$ rounds. LRU misses on every request, because three pages cycle through two slots, so it pays $12$ in each round, $12 r$ in total. The optimum keeps $c$ in one slot and alternates $a$ and $b$ in the other. It pays $12$ in the first round and $2$ in each later round, and in the last round it can evict $c$ instead of $a$, which saves $1$. A brute-force search gives these costs:

| rounds $r$ | LRU | GreedyDual | optimum |
|---|---|---|---|
| 1 | 12 | 12 | 12 |
| 2 | 24 | 14 | 13 |
| 5 | 60 | 20 | 19 |
| 20 | 240 | 50 | 49 |

So the optimum is $2r + 9$ for $r \ge 2$ and LRU pays $12 r$. If the cost of $c$ is $M$ instead of $10$, LRU pays $(M + 2) r$ and the optimum about $2 r$, so the ratio of LRU tends to $(M + 2) / 2$, which has no bound when $M$ grows.

**GreedyDual on the same sequence.** GreedyDual gives a page the credit $w_p$ when it is loaded or requested. On a miss with a full cache it evicts a page with the least credit and subtracts that credit from all pages in the cache. In round $1$, $b$ arrives when $c$ has credit $10$ and $a$ has credit $1$, so $a$ is evicted and $c$ falls to $9$. Each later round requests $c$ while it is still in the cache and resets its credit to $10$, so $c$ is never evicted, and GreedyDual pays $2$ in each round after the first. Its cost $2r + 10$ is within $1$ of the optimum.

## Known algorithms

- **Double coverage on a star (Chrobak, Karloff, Payne and Vishwanathan 1991).** The first $k$-competitive deterministic algorithm. With the star view above, [double coverage](/double-coverage/) on trees moves all servers that have no other server between them and the request toward it at the same speed.
- **GreedyDual (Young 1994).** The credit rule above, [Landlord](/landlord-algorithm/) with unit sizes. It is $k$-competitive, and $k/(k - h + 1)$-competitive against an optimum with $h$ slots. It is simple, and with a priority queue each request takes $O(\log k)$ time. The systems page is [GreedyDual](/greedy-dual/), and [GDSF](/gdsf/) is a variant for web caches.
- **The work function algorithm.** It is $k$-competitive on weighted stars (Bartal and Koutsoupias 2004), but it costs much more time for each request.
- **Randomized primal-dual (Bansal, Buchbinder and Naor 2007).** An [online primal-dual](/online-primal-dual/) algorithm keeps a fractional solution of a linear program for weighted paging, with a multiplicative update, and is $O(\log k)$-competitive for the fractional problem. An online rounding turns it into a randomized algorithm that loses only a constant factor. So the randomized ratio is $O(\log k)$.
- **Generalized caching.** Landlord is $k$-competitive for any sizes and costs (Young 2002; Cao and Irani 1997 for GreedyDual-Size). Bansal, Buchbinder and Naor gave a randomized $O(\log^2 k)$ bound in 2008, and Adamaszek, Czumaj, Englert and Räcke (2012) gave $O(\log k)$.

## Bounds

**Deterministic, lower bound $k$.** Paging is the case with all costs equal, and every deterministic paging algorithm has ratio at least $k$ ([Sleator and Tarjan 1985](/sleator-tarjan-paging-bound/)). So no deterministic algorithm is better than $k$-competitive for weighted paging.

**Deterministic, upper bound $k$.** GreedyDual and double coverage on a star are $k$-competitive. The proof for GreedyDual, with the potential $(h - 1) \sum_{p \in \mathrm{ALG}} \mathrm{credit}(p) + k \sum_{p \in \mathrm{OPT}} (w_p - \mathrm{credit}(p))$, where the sums are over the pages in each cache, is on the [Landlord](/landlord-algorithm/) page, and the proof for double coverage on trees is on the double coverage page. So the deterministic ratio is exactly $k$.

**Randomized.** For paging, the best randomized ratio is $H_k = \ln k + O(1)$ against an oblivious adversary (the lower bound of Fiat, Karp, Luby, McGeoch, Sleator and Young, see the [paging lower bound](/online-caching-lower-bound/)). So weighted paging needs $\Omega(\log k)$, and the algorithm of Bansal, Buchbinder and Naor gives $O(\log k)$. The randomized ratio is $\Theta(\log k)$, but the exact constant is not known. Simple randomized rules do not work: [randomized marking](/randomized-marking/) ignores the costs. On the example above it evicts $c$ with probability $1/2$ in some phases, so its expected cost grows with $M$ while the optimum does not.

**The offline problem.** With unit sizes, the offline optimum is a minimum-cost flow, so it can be computed in polynomial time. With different sizes, generalized caching is NP-hard even in the fault model (Chrobak, Woeginger, Makino and Xu 2012), and Bar-Noy, Bar-Yehuda, Freund, Naor and Schieber (2001) gave a $4$-approximation. Belady's rule, evict the page whose next request is furthest, is not optimal when the costs differ: in the example above, at the miss on $a$ in round $2$ the cache holds $c$ and $b$, and $b$ comes back first, so Belady's rule evicts $c$ and later pays $10$ to load it again. A script gives $121$ for Belady's rule and $49$ for the optimum with $r = 20$ rounds.

## Reductions

- **To the $k$-server problem.** Weighted paging is $k$-server on a weighted star, so each $k$-server algorithm for trees gives a weighted paging algorithm with the same ratio.
- **From paging.** Paging is weighted paging with unit costs, so each paging lower bound holds here.
- **To a covering linear program.** For each page $p$ and each interval between two requests of $p$, a variable says how much of $p$ is evicted in that interval. The constraint for each time says that at least $(\text{the number of distinct pages so far}) - k$ pages are out of the cache. This program is the base of the primal-dual algorithm, and Young's analysis of GreedyDual uses its dual.

## Applications

- **Web and content caches.** Objects come from servers with different latencies or costs. GreedyDual-Size and its variants, such as [GDSF](/gdsf/), are used in web proxies.
- **Database buffers and storage tiers.** Pages that are expensive to recompute or to fetch from a slow tier get higher weights.
- **Distributed systems.** In a cache of remote data, the cost of a miss depends on the distance to the source, which is the motivating model of the star view.

## References
