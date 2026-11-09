---
tag: 3V15JW
kind: problem
slug: golomb-ruler-problem
name: Golomb ruler problem
aliases:
- optimal Golomb ruler
area: combinatorics/exhaustive-search
level: advanced
summary: Find the shortest ruler with n integer marks such that all distances between pairs of marks are distinct.
prereqs: [generic-backtracking-algorithm, search-space, constraint-satisfaction-problem]
see_also: [generic-backtracking-algorithm, all-different-constraint, symmetry-breaking, constraint-programming, combinatorial-explosion, search-tree-pruning, n-queens-problem, brute-force-search]
sources:
  - url: https://oeis.org/A003022
    title: OEIS A003022, length of the shortest Golomb ruler with n marks
    locator: the table of values and the history of the optimality proofs
  - url: https://www.distributed.net/OGR
    title: distributed.net, Optimal Golomb Ruler project
    locator: the project pages for OGR-24 to OGR-28
  - paper: "Paul Erdős and Pál Turán, On a problem of Sidon in additive number theory, and on some related problems, Journal of the London Mathematical Society 16, 1941, 212 to 215"
    locator: the upper bound on the size of a Sidon set in an interval, which gives the lower bound on the length of a ruler
  - paper: "James Singer, A theorem in finite projective geometry and some applications to number theory, Transactions of the American Mathematical Society 43, 1938, 377 to 385"
    locator: the perfect difference sets, which give rulers with q + 1 marks and length less than q^2 + q + 1
  - paper: "Wallace C. Babcock, Intermodulation interference in radio systems, Bell System Technical Journal 32(1), 1953, 63 to 73"
    locator: the choice of channel frequencies with distinct differences, the first engineering use of these rulers
  - url: https://www.csplib.org/Problems/prob006/
    title: CSPLib problem 006, Golomb rulers
    locator: the constraint model and its use as a benchmark
---

A *Golomb ruler* is a set of integer marks $0 = a_1 < a_2 < \cdots < a_n$ in which no two pairs of marks are the same distance apart. Its length is the last mark $a_n$, and the Golomb ruler problem asks for the shortest ruler with $n$ marks. The answers $0, 1, 3, 6, 11, 17, 25, 34, 44, 55, \ldots$ have no known formula, so each one is found by an exhaustive [backtracking](/generic-backtracking-algorithm/) search and then proved optimal by finishing the search. Since the search space grows very fast, the optimal rulers with 24 to 28 marks needed years of volunteer computing by distributed.net.

## In plain words

Put marks on a stick at whole-number positions, always including both ends. Measure the distance between every pair of marks. The marks form a Golomb ruler if no distance appears twice.

The marks 0, 1, 4 and 6 work: the distances are 1, 2, 3, 4, 5 and 6, each once. With five marks it is not possible to stay at length 10, and the best length is 11.

The problem is to find, for a given number of marks, the shortest stick that works. No formula gives the answer. Computers find it by trying positions mark by mark, stopping early when two distances clash, and then checking every shorter stick to show that none works.

## Definition

A *Golomb ruler with $n$ marks* is a set $A = \{a_1, \ldots, a_n\}$ of integers with $0 = a_1 < a_2 < \cdots < a_n$ such that the $\binom{n}{2}$ differences $a_j - a_i$ with $i < j$ are pairwise distinct. Its *length* is $a_n$.

- The *optimization problem* asks, given $n$, for a ruler of minimum length $G(n)$. Such a ruler is an *optimal Golomb ruler* (OGR).
- The *decision problem* asks, given $n$ and $L$, whether a ruler with $n$ marks and length at most $L$ exists.

A ruler and its mirror image $\{a_n - a_i\}$ have the same length, so optimal rulers come in mirror pairs, and a ruler is usually counted once up to this symmetry. A set with distinct differences is the same as a *Sidon set*: a set in which all sums $a_i + a_j$ with $i \le j$ are distinct, since $a_i + a_j = a_k + a_l$ exactly when $a_i - a_k = a_l - a_j$.

## Variants

- **Fixed length.** Given $L$, find the largest number of marks in $[0, L]$ with distinct differences. This is the largest Sidon subset of an interval.
- **Perfect rulers.** A ruler is *perfect* if its differences are exactly $1, 2, \ldots, a_n$. Perfect Golomb rulers exist only for $n \le 4$.
- **Near-optimal rulers.** Fast constructions give rulers whose length is close to optimal for very large $n$, where exact search is out of reach.
- **Modular rulers.** Ask for distinct differences modulo $m$. Perfect difference sets are the case in which every nonzero residue appears once.
- **Two dimensions.** Golomb rectangles ask for points in a grid with distinct difference vectors. Costas arrays are a special case with one point in each row and column.

## Examples

Optimal lengths for small $n$ (OEIS A003022), with one optimal ruler for each:

| $n$ | $G(n)$ | an optimal ruler |
|---|---|---|
| 1 | 0 | 0 |
| 2 | 1 | 0, 1 |
| 3 | 3 | 0, 1, 3 |
| 4 | 6 | 0, 1, 4, 6 |
| 5 | 11 | 0, 1, 4, 9, 11 |
| 6 | 17 | 0, 1, 4, 10, 12, 17 |
| 7 | 25 | 0, 1, 4, 10, 18, 23, 25 |
| 8 | 34 | 0, 1, 4, 9, 15, 22, 32, 34 |
| 9 | 44 | 0, 1, 5, 12, 25, 27, 35, 41, 44 |
| 10 | 55 | 0, 1, 6, 10, 23, 26, 34, 41, 53, 55 |

The next values are $G(11) = 72$ and $G(12) = 85$, and the largest known value is $G(28) = 585$.

**Five marks.** The ruler $0, 1, 4, 9, 11$ has the differences $1, 4, 9, 11, 3, 8, 10, 5, 7, 2$, all distinct. Only the distance 6 is missing. With 10 differences, a ruler of length 10 would have to be perfect, and none is, so 11 is optimal.

**A non-example.** The marks $0, 1, 2, 4$ are not a Golomb ruler: the distance 1 appears twice, between 0 and 1 and between 1 and 2.

## Known algorithms

- **Backtracking.** Place the marks from left to right. Keep the set of distances used so far, often as a bit mask, and reject a new mark as soon as one of its distances to the earlier marks is already used. To find $G(n)$, run the search with $L = \binom{n}{2}, \binom{n}{2} + 1, \ldots$ until it succeeds. A plain Python version of this search finds $G(9)$ in a few seconds and $G(10)$ in under a minute, and each extra mark costs about ten times more.
- **Pruning.** If $r$ marks remain to be placed, the remaining gaps are distinct, so the rest of the ruler needs length at least $1 + 2 + \cdots + r$. Sharper bounds use the smallest unused distances. Mirror symmetry is broken by asking that the first gap be smaller than the last gap. See [search tree pruning](/search-tree-pruning/) and [symmetry breaking](/symmetry-breaking/).
- **Constraint programming.** Model the marks as variables, the differences as auxiliary variables, and state an [all-different constraint](/all-different-constraint/) on the differences. The problem is a standard benchmark in this field, as CSPLib problem 006.
- **Distributed search.** The distributed.net project split the search tree for 24 to 28 marks into many small pieces and ran them on volunteer computers, with a highly tuned bit-mask search at each leaf. The proof for 28 marks ended in 2022.
- **Algebraic constructions.** The constructions of Singer, of Bose, and of Ruzsa give good rulers for many $n$ in polynomial time, but they do not prove optimality. They give the starting bound $L$ for exact searches.

The complexity of the problem is not settled: no polynomial algorithm is known, and no NP-hardness proof for computing $G(n)$ is known either.

## Bounds

**Simple lower bound.** The $\binom{n}{2}$ differences are distinct positive integers no larger than $a_n$, so $G(n) \ge \binom{n}{2}$. Equality holds only for perfect rulers, so for $n \ge 5$ the bound is strict.

**Erdős and Turán.** A Sidon set in $\{1, \ldots, N\}$ has at most $\sqrt{N} + O(N^{1/4})$ elements (1941). So $G(n) \ge n^2 - O(n^{3/2})$.

**Upper bound.** For each prime power $q$, Singer's perfect difference sets give a ruler with $q + 1$ marks and length less than $q^2 + q + 1$. With the density of primes, this gives $G(n) \le n^2 (1 + o(1))$. Together with the lower bound, $G(n) \sim n^2$.

**Cost of exact search.** The search space for $n$ marks and length $L$ has $\binom{L-1}{n-2}$ placements before pruning, and $L$ is close to $n^2$. Pruning cuts this by a huge factor, but the work still grows faster than exponentially in practice, which is why each new value has taken years.

## Reductions

- **Fixed length to optimal length.** $G(n)$ is the least $L$ for which the fixed-length problem gives at least $n$ marks, so either problem solves the other by a scan over $L$ or over $n$.
- **To constraint satisfaction.** A model with variables $a_1, \ldots, a_n$, ordering constraints and an all-different constraint over the differences is a [constraint satisfaction problem](/constraint-satisfaction-problem/).
- **To integer programming.** Binary variables $x_p$ for each position $p \le L$, with one constraint for each distance $d$ that at most one pair at distance $d$ is chosen, give a $0/1$ program for the fixed-length variant.

## Applications

- **Radio frequencies.** Babcock (1953) chose channel frequencies with distinct differences so that the intermodulation products of two channels do not fall on a third channel.
- **Antenna arrays.** In radio astronomy and radar, antennas placed at the marks of a Golomb ruler measure each spacing once, which gives many distinct baselines with few antennas.
- **Codes.** Self-orthogonal convolutional codes and some optical codes use sets with distinct differences.
- **Benchmarks.** The problem is a standard test for backtracking, constraint solvers and parallel search, because the instances are short to state and hard to solve.

## References
