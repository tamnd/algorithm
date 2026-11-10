---
tag: 4VVMCV
kind: definition
slug: offline-algorithm
name: Offline algorithm
aliases:
- off-line algorithm
area: online-and-streaming/competitive-analysis
level: intro
summary: An algorithm that sees the entire input before producing its output.
prereqs: [online-algorithm]
see_also: [online-algorithm, offline-optimum, competitive-ratio, belady-algorithm, request-answer-game, advice-model]
sources:
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1 (online and offline algorithms, the optimal offline algorithm OPT)
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the off-line rules used as the yardstick for the on-line rules
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the replacement rule MIN, which uses the future requests
---

An offline algorithm receives the whole input before it must produce any part of its output. In online computation the word marks the contrast with an [online algorithm](/online-algorithm/): on a request sequence $\sigma = r_1 \cdots r_n$, an offline algorithm may choose the answer to $r_i$ with knowledge of all of $r_1, \ldots, r_n$. The best offline algorithm defines the [offline optimum](/offline-optimum/), the yardstick of the [competitive ratio](/competitive-ratio/).

## Definition

Fix a request set $R$, an answer set $A$ and, for each $n \ge 0$, a cost function $f_n : R^n \times A^n \to \mathbb{R}_{\ge 0} \cup \{\infty\}$, as in a [request-answer game](/request-answer-game/). An answer sequence with cost $\infty$ is not feasible.

An **offline algorithm** is a map $\Phi$ that sends each finite sequence $\sigma = r_1 \cdots r_n \in R^n$ to an answer sequence $\Phi(\sigma) = a_1 \cdots a_n \in A^n$. Its cost on $\sigma$ is $f_n(\sigma, \Phi(\sigma))$. No condition links $a_i$ to the requests after $r_i$: the answer $a_i$ may depend on all of $\sigma$, including its length $n$.

An **online algorithm** is the special case where $a_i$ depends only on $r_1, \ldots, r_i$: there are functions $g_i : R^i \to A$ with $a_i = g_i(r_1, \ldots, r_i)$ for every $\sigma$ and every $i \le n$. So each online algorithm is an offline algorithm, and the converse is false.

An offline algorithm is **optimal** if, for every $\sigma$, its cost equals $\min_{a \in A^n} f_n(\sigma, a)$. This value is the offline optimum $\mathrm{OPT}(\sigma)$. The definition counts information only. An offline algorithm may be slow, and in competitive analysis the optimal offline algorithm is often not computable in polynomial time. Only its cost matters.

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of an algorithm and of the optimal offline solution on $\sigma$.

## Examples and non-examples

- **Belady's rule (example).** For [paging](/paging-problem/) with a cache of $k$ pages, [Belady's algorithm](/belady-algorithm/) evicts the page whose next request is furthest in the future. It reads requests after the current one, so it is offline, and it is optimal. On $\sigma = 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$ with $k = 3$ and an empty start, it makes 7 faults. [LRU](/lru/) makes 10 faults on the same sequence.
- **Ski rental (example).** In [ski rental](/ski-rental-problem/), the offline algorithm knows the number $n$ of ski days. It buys on day 1 if $n \ge B$ and rents every day otherwise, so it pays $\min(n, B)$.
- **Sorting (example).** [Merge sort](/merge-sort/) reads all items before it writes the first output item. In the language of this page it is offline.
- **LRU (non-example).** LRU decides each eviction from the past requests only. It is an online algorithm. As an offline algorithm it is allowed but not optimal.
- **An algorithm that knows only the length (non-example).** A rule that knows $n$ in advance but not the requests is between the two models. It is a semi-online algorithm. In the [advice model](/advice-model/) this knowledge costs $O(\log n)$ bits of advice.
- **An algorithm with lookahead (non-example).** A paging rule that sees the next $\ell$ requests is not online and not fully offline. For paging, a fixed lookahead does not lower the deterministic competitive ratio: the adversary repeats each request $\ell + 1$ times, so the lookahead shows only copies of the current request, and the repeats cause no faults.

## Related definitions

- **[Online algorithm](/online-algorithm/).** The answer to each request depends only on the requests so far.
- **[Offline optimum](/offline-optimum/).** The cost $\mathrm{OPT}(\sigma)$ of an optimal offline algorithm on $\sigma$.
- **[Competitive ratio](/competitive-ratio/).** The smallest $c$ with $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$. It measures the price of being online.
- **[Adaptive offline adversary](/adaptive-offline-adversary/).** An adversary that builds the request sequence step by step and then serves it with an optimal offline algorithm.
- **[Advice model](/advice-model/).** An online algorithm that may read bits written by an oracle that knows $\sigma$. With enough bits it can follow an optimal offline algorithm.

## References
