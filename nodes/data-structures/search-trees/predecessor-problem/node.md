---
tag: E2JG2M
kind: problem
slug: predecessor-problem
name: Predecessor problem
aliases:
- successor problem
area: data-structures/search-trees
level: advanced
summary: Find the largest key not exceeding a query value in a dynamic set.
prereqs: [floor-and-ceiling-in-ordered-set, word-ram, ordered-set]
see_also: [fusion-tree, predecessor-lower-bound, integer-sorting, priority-queue, longest-prefix-match, cell-probe-model, hash-table, bit-vector]
sources:
  - paper: doi:10.1016/0020-0190(77)90031-x
    title: Peter van Emde Boas, Preserving order in a forest in less than logarithmic time and linear space, Information Processing Letters 6(3), 1977
    locator: pages 80 to 82
  - paper: doi:10.1016/0020-0190(83)90075-3
    title: Dan E. Willard, Log-logarithmic worst-case range queries are possible in space Θ(N), Information Processing Letters 17(2), 1983
    locator: pages 81 to 84
  - paper: doi:10.1016/0022-0000(93)90040-4
    title: Michael L. Fredman and Dan E. Willard, Surpassing the information theoretic bound with fusion trees, Journal of Computer and System Sciences 47(3), 1993
    locator: pages 424 to 436
  - paper: doi:10.1145/1132516.1132551
    title: Mihai Pătraşcu and Mikkel Thorup, Time-space trade-offs for predecessor search, STOC 2006
    locator: the whole paper
---

The predecessor problem asks to keep a set $S$ of $n$ integers from the universe $\{0, 1, \ldots, 2^w - 1\}$ and to answer, for a query $x$, the largest element of $S$ that is at most $x$. It is the [floor query](/floor-and-ceiling-in-ordered-set/) for integer keys on the [word RAM](/word-ram/), where a key fits in one machine word of $w$ bits. With comparisons alone the answer costs $\Theta(\log n)$, but word operations do better: the van Emde Boas structure takes $O(\log w)$ time, the [fusion tree](/fusion-tree/) takes $O(\log n / \log w)$ time, and Pătraşcu and Thorup (2006) found the exact trade-off between time and space for the static problem.

## In plain words

You keep a set of whole numbers, all below some fixed limit such as $2^{64}$. For a number $x$, you want the closest number of the set that is not above $x$. The set may change as you go.

A search tree finds the answer by comparing numbers, and it needs about $\log n$ comparisons. But a computer can do more than compare: it can look at the bits of a number, split a number into parts, and do arithmetic on many small fields of a word at once. With such tricks the answer can come faster than any method that only compares.

## Definition

Fix the word size $w$ and the universe $U = \{0, 1, \ldots, u - 1\}$ with $u = 2^w$. A set $S \subseteq U$ with $|S| = n$ is given. The operations are:

- $\mathrm{pred}_S(x) = \max\{y \in S : y \le x\}$, or NIL if no such $y$;
- $\mathrm{succ}_S(x) = \min\{y \in S : y \ge x\}$, or NIL;
- in the dynamic problem also $\mathrm{insert}(x)$ and $\mathrm{delete}(x)$.

The model is the word RAM with words of $w \ge \lg n$ bits and unit-cost addition, subtraction, comparison, bitwise operations, shifts and, in most results, multiplication. Space is counted in words. Some authors define $\mathrm{pred}$ with $y < x$; the two forms differ by one membership test, which a [hash table](/hash-table/) does in $O(1)$ expected time.

## Variants

- **Static.** $S$ is given once; the cost is the query time as a function of the space and of the preprocessing time.
- **Dynamic.** Inserts and deletes as well, with worst-case, amortized or expected bounds.
- **Successor, strict forms, rank.** Successor is symmetric. With rank, the query returns the number of keys $\le x$ as well; this is harder in some dynamic settings.
- **Range emptiness.** Decide whether $S \cap [a, b]$ is empty. One successor query answers it, and the problem can be easier than predecessor search.
- **Cell-probe version.** Count only memory accesses, with cells of $w$ bits, as in the [cell-probe model](/cell-probe-model/). Lower bounds are proved here.
- **Comparison version.** Keys from an arbitrary total order: the [floor and ceiling problem](/floor-and-ceiling-in-ordered-set/), with $\Theta(\log n)$ comparisons.

## Examples

Let $w = 4$, so $U = \{0, \ldots, 15\}$, and $S = \{2, 5, 11, 12\}$, in binary $0010$, $0101$, $1011$, $1100$.

| $x$ | $\mathrm{pred}_S(x)$ | $\mathrm{succ}_S(x)$ |
|---|---|---|
| 1 | NIL | 2 |
| 5 | 5 | 5 |
| 10 | 5 | 11 |
| 13 | 12 | NIL |

**The query for 10 by prefixes.** In binary, $x = 1010$. Its prefixes are $1$, $10$, $101$ and $1010$. The prefixes of the keys of $S$ are stored in a hash table, one table per length. Binary search on the length: the prefix $10$ is a prefix of $1011$, so the search goes longer; $101$ is also present; $1010$ is not. So the longest common prefix of $x$ and a key is $101$, of length 3. Below $101$, only the key $1011$ exists, and $x$ goes to the side of the missing branch $1010$, which is to the left. So the answer is the key just before $1011$ in sorted order, which is $0101 = 5$. This search takes $O(\log w)$ hash lookups; it is the query of the x-fast trie of Willard (1983).

## Known algorithms

| method | query | update | space | notes |
|---|---|---|---|---|
| [binary search](/binary-search/) on a sorted array | $O(\log n)$ | $O(n)$ | $O(n)$ | comparisons only |
| balanced search tree | $O(\log n)$ | $O(\log n)$ | $O(n)$ | comparisons only |
| table of all answers | $O(1)$ | $O(u)$ | $O(u)$ | static in practice |
| [bit vector](/bit-vector/) with summary levels | $O(\log_w u) = O(1)$ for $u = w^{O(1)}$ | $O(\log_w u)$ | $O(u / w)$ | for small universes |
| van Emde Boas tree (1975, 1977) | $O(\log w)$ | $O(\log w)$ | $O(u)$ | deterministic |
| x-fast trie (Willard 1983) | $O(\log w)$ expected | $O(w)$ | $O(n w)$ | hash tables of prefixes |
| y-fast trie (Willard 1983) | $O(\log w)$ expected | $O(\log w)$ amortized expected | $O(n)$ | x-fast trie over buckets of $\Theta(w)$ keys |
| [fusion tree](/fusion-tree/) (Fredman and Willard 1993) | $O(\log_w n)$ | amortized | $O(n)$ | uses multiplication |

The van Emde Boas bound is good when $w$ is small relative to $n$, and the fusion tree bound when $w$ is large. Taking the better of the two gives $O(\min(\log w, \log n / \log w)) = O(\sqrt{\log n})$ for each $n$ and $w$, since the minimum is largest when $\log w = \sqrt{\log n}$. Better combined bounds come from exponential search trees of Andersson and Thorup and from the static structure of Beame and Fich.

## Bounds

- **Comparison model.** $\lceil \lg(n + 1) \rceil$ comparisons are needed and enough, by the decision tree argument on the [floor and ceiling](/floor-and-ceiling-in-ordered-set/) page.
- **Word RAM, static.** Pătraşcu and Thorup (2006) gave matching upper and lower bounds for static predecessor search with space $n \cdot 2^a$ words, as a minimum of four terms in $n$, $w$ and $a$. For near-linear space, one of the terms is $\log_w n$, the fusion tree bound, and another is close to $\log w$, the van Emde Boas bound, so each of the two classic structures is optimal in some range of $n$ and $w$. Their lower bounds are proved in the [cell-probe model](/cell-probe-model/), which counts only memory accesses, so no choice of word operations can beat them. See the [predecessor lower bound](/predecessor-lower-bound/).
- **Upper bound for all $n$ and $w$.** By the minimum of the van Emde Boas tree and the fusion tree, $O(\sqrt{\log n})$ time with $O(n)$ space, with hashing for the van Emde Boas part. This is below $\Theta(\log n)$, the comparison bound.

## Reductions

- **Sorting from dynamic predecessor.** Insert the $n$ keys, then walk with successor queries from $\mathrm{succ}(0)$. A dynamic predecessor structure with time $T(n)$ per operation gives [integer sorting](/integer-sorting/) in $O(n\,T(n))$ time. With the van Emde Boas tree this is $O(n \log w)$.
- **Priority queues.** A dynamic predecessor structure is a [priority queue](/priority-queue/): find-min is $\mathrm{succ}(0)$.
- **Range emptiness.** $S \cap [a, b] \ne \emptyset$ exactly when $\mathrm{succ}(a) \ne$ NIL and $\mathrm{succ}(a) \le b$.
- **Floor for other keys.** Strings of at most $w$ bits, padded to a fixed length, and floating-point numbers of one sign, map to integers that keep their order, so the integer structures apply to them.
- **Longest prefix match.** Each prefix of an IP routing table is an interval of addresses; after cutting the intervals at their end points, [longest prefix match](/longest-prefix-match/) becomes a predecessor query over at most $2n$ end points.

## Applications

- **Packet routing.** Longest prefix match on IP addresses, as above.
- **Integer sorting and priority queues.** Fast integer sorting and fast shortest paths with integer weights use predecessor structures as their core.
- **Databases and file systems.** Range queries on integer keys, such as time stamps, start with a successor query.
- **Computational geometry.** Plane sweeps on integer grids use predecessor structures to find the neighbours of a point on the sweep line.

## References
