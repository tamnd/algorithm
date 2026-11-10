---
tag: ZNRZ5J
kind: concept
slug: marking-phases
name: Marking phases
aliases:
- phase partitioning
- k-phase partition
- phase partition of a request sequence
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Splitting a request sequence into phases each containing k distinct pages, the basis of the standard paging analysis.
prereqs: [paging-problem]
see_also: [marking-algorithm, flush-when-full, randomized-marking, sleator-tarjan-paging-bound, harmonic-paging-bound, online-caching-lower-bound, belady-algorithm]
sources:
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the division of the request sequence into k-phases, the marking algorithms, and the bound on OPT by the new pages of each phase
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1 (k-phase partition and marking algorithms), and Chapter 4 (the analysis of MARK)
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the division of the sequence into blocks used in the bounds for LRU and FIFO
---

The marking phases of a request sequence, for a cache size $k$, are the blocks of the sequence cut greedily so that each block has exactly $k$ distinct pages, except perhaps the last one. The partition depends only on the sequence and on $k$, not on any algorithm. It gives the two bounds of the standard analysis of paging: a [marking algorithm](/marking-algorithm/) has at most $k$ faults in each phase, and the optimal offline algorithm has at least one fault for each pair of consecutive phases. Fiat, Karp, Luby, McGeoch, Sleator and Young used it in 1991 for the analysis of [randomized marking](/randomized-marking/).

## In plain words

Read the requests from the start and keep a list of the different pages seen. When a request would make the list one page too long for the cache, cut the sequence there, clear the list, and start a new phase with that request.

So each phase uses as many different pages as the cache holds. A good online rule keeps all of them once loaded, so it misses at most once per page in a phase.

The best rule that sees the future cannot do much better. Take the stretch from just after the start of one phase to the start of the next. Not counting the first page of the phase, it asks for as many different pages as the cache holds, and that first page is still in the cache. So one of these pages is missing, and even the best rule misses in each such stretch.

## The idea

**Definition.** Fix $k \ge 1$ and $\sigma = \sigma_1 \cdots \sigma_n$. Phase 1 starts at request 1. If phase $i$ starts at request $a_i$, it ends at the largest $b$ such that $\sigma_{a_i}, \ldots, \sigma_b$ contain at most $k$ distinct pages, and phase $i + 1$ starts at $a_{i+1} = b + 1$, if $b < n$. Let $N$ be the number of phases. So:

- each phase except perhaps the last has exactly $k$ distinct pages;
- the first request of phase $i + 1$ is a page that does not occur in phase $i$;
- one pass with a set of size at most $k$ computes the partition in $O(n)$ expected time.

**The upper bound for marking algorithms.** A [marking algorithm](/marking-algorithm/) marks each requested page, and it unmarks all pages exactly when a request finds all $k$ cached pages marked and missing. So its marks are the distinct pages of the current phase, and it never evicts a page of the current phase once that page has been requested. Each of the at most $k$ distinct pages of a phase faults at most once in that phase, so the algorithm has at most $kN$ faults.

**The lower bound for OPT.** For $1 \le i < N$, let $p_i = \sigma_{a_i}$ be the first page of phase $i$, and let the window $W_i$ be the requests from $a_i + 1$ to $a_{i+1}$.

**Claim.** Each algorithm, online or offline, has at least one fault in each window $W_i$. So with any initial cache it has at least $N - 1$ faults, and with an empty cache at least $N$ faults.

*Proof.* After request $a_i$, the cache holds $p_i$ and at most $k - 1$ other pages. Phase $i$ has $k$ distinct pages, so the requests $a_i + 1, \ldots, a_{i+1} - 1$ contain the $k - 1$ pages of phase $i$ other than $p_i$. The request $a_{i+1}$ is a page outside phase $i$, so it is not $p_i$ either. So $W_i$ requests at least $k$ distinct pages other than $p_i$. At most $k - 1$ of them are in the cache after request $a_i$, so one of them is missing. Take the first request in $W_i$ for a page that was missing after request $a_i$. Between them the algorithm can load the page only by paying 1, so in a [demand paging](/demand-paging/) algorithm this request is a fault, and in general there is a load in $W_i$. The windows $W_1, \ldots, W_{N-1}$ are disjoint, because $W_i$ ends at $a_{i+1}$ and $W_{i+1}$ starts at $a_{i+1} + 1$. With an empty start, request 1 is one more fault, and it is in no window. $\square$

**Together.** With an empty start, each marking algorithm has $\mathrm{ALG}(\sigma) \le kN \le k \cdot \mathrm{OPT}(\sigma)$. So it is strictly $k$-competitive. With a common initial cache, $\mathrm{ALG}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k$.

**New pages.** A page of phase $i \ge 2$ is *new* if it does not occur in phase $i - 1$, and *stale* if it does. Let $m_i$ be the number of new pages of phase $i$, with $m_1 = k$ when the cache starts empty. Phases $i - 1$ and $i$ together contain $k + m_i$ distinct pages, and the cache before phase $i - 1$ holds at most $k$ of them. So OPT has at least $m_i$ faults in phases $i - 1$ and $i$ together. Summing over $i$, each phase is counted at most twice, so

$$\mathrm{OPT}(\sigma) \ge \frac{1}{2} \sum_{i=1}^{N} m_i.$$

This finer bound is the base of the $2H_k$ analysis of [randomized marking](/randomized-marking/).

## Examples

Take $k = 3$ and $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$.

| phase $i$ | requests | distinct pages | new pages $m_i$ | window $W_i$ | pages of $W_i$ other than $p_i$ |
|---|---|---|---|---|---|
| 1 | $1\,2\,3$ | 1, 2, 3 | 3 | $2\,3\,4$ (requests 2 to 4) | 2, 3, 4 |
| 2 | $4\,1\,2$ | 4, 1, 2 | 1 | $1\,2\,5$ (requests 5 to 7) | 1, 2, 5 |
| 3 | $5\,1\,2$ | 5, 1, 2 | 1 | $1\,2\,3$ (requests 8 to 10) | 1, 2, 3 |
| 4 | $3\,4\,5$ | 3, 4, 5 | 2 | | |

There are $N = 4$ phases. A marking algorithm has at most $3 \cdot 4 = 12$ faults: [LRU](/lru/) has 10 and [flush when full](/flush-when-full/) has 12. OPT has at least 4 faults, and the new pages give $\frac{1}{2}(3 + 1 + 1 + 2) = 3.5$, so again at least 4. In fact $\mathrm{OPT} = 7$, with 5 faults forced by the 5 distinct pages.

**A tight case.** Take the cycle $1\,2\,\cdots\,(k+1)$ repeated. Each phase has $k$ requests, and each window of $k$ requests forces one fault of OPT. [Belady's algorithm](/belady-algorithm/) faults at most once in each $k$ requests after the first $k$, so OPT is close to $N$. LRU faults on each request, so it has $kN$ faults, and both bounds are reached up to an additive constant.

## Where it is used

- **Deterministic paging.** The proof that each [marking algorithm](/marking-algorithm/) is $k$-competitive, and so [LRU](/lru/) and [flush when full](/flush-when-full/), is the two bounds above. The [conservative](/cache-replacement-policy/) algorithms, such as FIFO, satisfy the same upper bound.
- **Resource augmentation.** With an optimal cache of $h \le k$ pages, each window forces $k - h + 1$ faults instead of one, which gives the ratio $k/(k - h + 1)$ of the [Sleator and Tarjan bound](/sleator-tarjan-paging-bound/).
- **Randomized paging.** The new and stale pages of each phase give the $2H_k$ bound of [randomized marking](/randomized-marking/), and the expected phase length on random requests gives the [harmonic lower bound](/harmonic-paging-bound/).
- **Learning-augmented paging.** [Learning-augmented marking](/learning-augmented-marking/) keeps the phase structure, and it uses predictions only to choose among the unmarked pages.

## References
