---
tag: VAEVWV
kind: theorem
slug: k-server-conjecture
name: k-server conjecture
aliases:
- Manasse-McGeoch-Sleator conjecture
area: online-and-streaming/paging-and-caching-online
level: research
summary: Conjectured that a deterministic k-competitive online algorithm exists for the k-server problem on every metric space; open in general.
prereqs: [k-server-problem, competitive-ratio, work-function-algorithm]
see_also: [double-coverage, work-function, sleator-tarjan-paging-bound, randomized-online-algorithm, metrical-task-systems, oblivious-adversary, online-caching-lower-bound]
sources:
  - paper: doi:10.1016/0196-6774(90)90003-W
    title: Mark S. Manasse, Lyle A. McGeoch and Daniel D. Sleator, Competitive algorithms for server problems, Journal of Algorithms 11(2), 1990, 208-230
    locator: the statement of the conjecture, the lower bound k, and the k-competitive algorithms for k = 2 and for k + 1 points
  - paper: doi:10.1145/210118.210128
    title: Elias Koutsoupias and Christos H. Papadimitriou, On the k-server conjecture, Journal of the ACM 42(5), 1995, 971-983
    locator: the bound 2k - 1 for the work function algorithm on every metric space
  - paper: doi:10.1016/j.cosrev.2009.04.002
    title: Elias Koutsoupias, The k-server problem, Computer Science Review 3(2), 2009, 105-118
    locator: the list of the special cases where the conjecture is known, and the randomized conjecture
  - paper: "Yair Bartal and Elias Koutsoupias, On the competitive ratio of the work function algorithm for the k-server problem, Theoretical Computer Science 324(2-3), 2004, 337-345"
    locator: the work function algorithm is k-competitive on the line, on weighted stars, and on metrics with k + 2 points
  - paper: doi:10.1137/0220008
    title: Marek Chrobak and Lawrence L. Larmore, An optimal on-line algorithm for k servers on trees, SIAM Journal on Computing 20(1), 1991, 144-148
    locator: double coverage is k-competitive on tree metrics
  - paper: doi:10.1145/3564246.3585132
    title: Sébastien Bubeck, Christian Coester and Yuval Rabani, The randomized k-server conjecture is false!, Proceedings of STOC 2023
    locator: metrics with k + 1 points where every randomized algorithm has ratio Ω(log^2 k), and the consequence Ω(log^2 n) for metrical task systems; arXiv:2211.05753
  - paper: doi:10.1145/2786.2793
    title: Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2), 1985, 202-208
    locator: LRU and FIFO are k-competitive for paging, the uniform case
---

The $k$-server conjecture says that for each metric space and each $k$, there is a deterministic online algorithm for the [$k$-server problem](/k-server-problem/) with competitive ratio $k$. Manasse, McGeoch and Sleator stated it in 1988, together with a proof that no deterministic algorithm can do better than $k$ on a space with more than $k$ points. So the conjecture says that this lower bound is always tight. It is known for many special cases, and the best proved bound for all metric spaces is $2k - 1$, by the [work function algorithm](/work-function-algorithm/). The randomized form of the conjecture, a ratio of $O(\log k)$ on every metric, was refuted in 2023.

## Statement

**Conjecture (Manasse, McGeoch and Sleator).** For every metric space $M$, every $k \ge 1$ and every start configuration, there is a deterministic online algorithm $A$ and a constant $b$ such that $A(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + b$ for all request sequences $\sigma$.

The constant $b$ may depend on $M$, $k$ and the start configuration, but not on $\sigma$. Together with the lower bound of Manasse, McGeoch and Sleator, the conjecture says that the deterministic competitive ratio of the $k$-server problem is exactly $k$ on each metric space with at least $k + 1$ points.

**What is proved.** The conjecture is true in these cases:

| case | algorithm | source |
|---|---|---|
| uniform metric (paging) | LRU, FIFO, each marking algorithm | Sleator and Tarjan 1985 |
| $k = 2$, every metric | an algorithm of MMS; also WFA | MMS 1990; Chrobak and Larmore 1992 |
| metrics with $k + 1$ points | an algorithm of MMS; also WFA | MMS 1990 |
| the line | [double coverage](/double-coverage/) | Chrobak, Karloff, Payne and Vishwanathan 1991 |
| tree metrics, including weighted stars | double coverage | Chrobak and Larmore 1991 |
| the line, weighted stars, metrics with $k + 2$ points | WFA | Bartal and Koutsoupias 2004 |

**The general bound.** For every metric space, the work function algorithm satisfies $\mathrm{WFA}(\sigma) \le (2k - 1) \cdot \mathrm{OPT}(\sigma) + b$ (Koutsoupias and Papadimitriou 1995). Before that, Fiat, Rabani and Ravid (1990) gave the first bound that depends only on $k$, and it grows exponentially in $k$. The *work function conjecture* is the stronger claim that WFA itself is $k$-competitive on every metric.

**The randomized conjecture.** Against an [oblivious adversary](/oblivious-adversary/), the folklore conjecture was that a randomized ratio of $O(\log k)$ is possible on every metric space, as it is on the uniform metric, where the best ratio is $H_k$. Bubeck, Coester and Rabani (2023) refuted it: there are metric spaces with $k + 1$ points on which every randomized online algorithm has ratio $\Omega(\log^2 k)$.

## In plain words

When $k$ servers move in a space, a simple trick shows that every online rule can be forced to pay $k$ times as much as the best plan. The conjecture says that this is the worst that can happen: on any space, there is a rule that never pays more than $k$ times the best plan, plus a fixed amount.

For caches, for points on a line, for trees and for two servers, people found such rules long ago. For general spaces, the best rule known pays at most about twice that, $2k - 1$ times the best plan. Closing the gap between $k$ and $2k - 1$ is one of the main open problems of online algorithms. For rules that may flip coins, people believed that a much smaller factor, about $\log k$, was always possible, but in 2023 this was shown to be false.

## Proof

The conjecture is open in general. This section proves the uniform case in full, and points to full proofs of the other parts on other pages.

**Theorem 1 (the lower bound).** On each metric space with at least $k + 1$ points, with the servers on $k$ distinct points at the start, no deterministic online algorithm is $c$-competitive for $c < k$. The full proof is Theorem 2 of the [$k$-server problem](/k-server-problem/) page: the adversary always requests the one point of a set of $k + 1$ points that the algorithm does not cover, and $k$ offline algorithms with different holes share the cost of the online algorithm.

**Theorem 2 (the uniform case).** On the uniform metric, LRU satisfies $\mathrm{LRU}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k$ for every start configuration with $k$ distinct points.

*Proof.* On the uniform metric, a lazy algorithm pays $1$ for each request that is not covered, a miss, so this is paging with a cache of $k$ pages. Split $\sigma$ into phases: phase $1$ starts at the first request, and each phase is the longest run of requests that has at most $k$ distinct pages. So a new phase starts at a request to the $(k+1)$-th distinct page since the start of the current phase. Let $P$ be the number of phases.

*LRU misses at most $k$ times in each phase.* Assume that LRU evicts a page $q$ in phase $r$, at a miss on $x$, and that $q$ was requested earlier in phase $r$. The other $k - 1$ pages in the cache were used after $q$, so they were also requested in phase $r$. Then the $k$ cached pages and $x$ are $k + 1$ distinct pages of phase $r$, which is not possible. So each page requested in a phase stays in the cache until the phase ends, and each miss of the phase is the first request to one of its at most $k$ distinct pages.

*The optimum misses at least $P - 1$ times.* For $r < P$, let $p$ be the first page of phase $r$. From the second request of phase $r$ up to the first request of phase $r + 1$, there are $k$ distinct pages other than $p$: the $k - 1$ others of phase $r$, and the page that starts phase $r + 1$. Each algorithm holds $p$ just after its request, so at most $k - 1$ of these $k$ pages are in its cache, and it misses at least once in this window. The windows for $r = 1, \ldots, P - 1$ are disjoint.

So $\mathrm{LRU}(\sigma) \le k P \le k (\mathrm{OPT}(\sigma) + 1)$. $\square$

The same proof works for each *marking algorithm*, a rule that never evicts a page requested in the current phase. FIFO is not a marking algorithm, but Sleator and Tarjan prove the same bound for it.

**Theorem 3 ($k + 1$ points).** If $|M| = k + 1$, then $\mathrm{WFA}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k \Delta$, where $\Delta$ is the diameter. The full proof is Theorem 2 on the [work function algorithm](/work-function-algorithm/) page.

**Theorem 4 (the line and trees).** On the line and on trees, double coverage is $k$-competitive. The full proof, with the potential $k M + \sum_{i < j} d(s_i, s_j)$, where $M$ is the cost of a minimum matching between the servers of the algorithm and those of the optimum, is on the [double coverage](/double-coverage/) page.

**Theorem 5 ($2k - 1$).** For every metric space, WFA is $(2k - 1)$-competitive. A sketch of the proof of Koutsoupias and Papadimitriou, with quasiconvexity and the duality lemma, is on the [work function algorithm](/work-function-algorithm/) page. $\blacksquare$

## Consequences

- **Paging.** Theorem 1 on the uniform metric gives the lower bound $k$ for deterministic paging, and Theorem 2 shows that LRU meets it.
- **Weighted paging.** Weighted paging is the $k$-server problem on a weighted star, a tree, so double coverage gives a $k$-competitive rule. This is the result of Chrobak, Karloff, Payne and Vishwanathan for the [weighted paging problem](/weighted-paging-problem/).
- **Metrical task systems.** The refutation of the randomized conjecture also gives $\Omega(\log^2 n)$ for randomized [metrical task systems](/metrical-task-systems/) on some $n$-point metrics, which matches the known upper bound $O(\log^2 n)$.
- **Methods.** Work at the conjecture produced the [work function](/work-function/) method, potential functions for online algorithms, and, for randomized algorithms, tree embeddings and online mirror descent.

## Tightness

The value $k$ cannot be lowered: Theorem 1 holds on every metric space with at least $k + 1$ points. On a space with at most $k$ points, the servers can cover all points, so the ratio is $1$ after a bounded cost.

The gap between $k$ and $2k - 1$ is open for general metrics. Before 2026, it was open even for $k = 3$ on general metrics. A 2026 preprint by Coester, Koutsoupias and Zbysiński (arXiv:2609.15979) claims a proof that WFA is $k$-competitive on every metric space, which would prove the conjecture. As of November 2026 it has not been refereed, and this page treats the conjecture as open.

For randomized algorithms, $H_k$ is tight on the uniform metric, but Bubeck, Coester and Rabani show that some metrics need $\Omega(\log^2 k)$. The best general lower bound for every metric with more than $k$ points is $\Omega(\log k / \log \log k)$, and the best general upper bounds are polylogarithmic in $k$ and in the number of points.

## History

Manasse, McGeoch and Sleator defined the $k$-server problem at STOC 1988 and stated the conjecture there; the journal version appeared in 1990. Fiat, Rabani and Ravid (1990) gave the first algorithm with a ratio that depends only on $k$. Chrobak, Karloff, Payne and Vishwanathan (1991) found double coverage for the line, and Chrobak and Larmore (1991) extended it to trees. Koutsoupias and Papadimitriou proved the bound $2k - 1$ for the work function algorithm in 1994, with the journal version in 1995, and that bound has not been improved for general metrics since. Bartal and Koutsoupias (2004) proved that WFA is $k$-competitive on more special metrics. The randomized conjecture was refuted by Bubeck, Coester and Rabani at STOC 2023.

## References
