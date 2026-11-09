---
tag: N12T4H
kind: concept
slug: combinatorial-explosion
name: Combinatorial explosion
aliases:
- exponential blow-up
- state explosion
area: combinatorics/exhaustive-search
level: intro
summary: The growth of the search space as the input size increases, which makes brute force infeasible.
prereqs: [search-space, asymptotic-notation]
see_also: [brute-force-search, search-space, exact-exponential-algorithms, stirling-approximation, factorial, polynomial-time, search-tree-pruning, np-complete]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, 1979
    locator: Chapter 1, Section 1.3 (polynomial time algorithms and intractable problems, the tables of running times and of the effect of faster computers)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.1, Computational tractability (brute-force search over an exponential space)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2, Backtrack programming (the size of backtrack trees and how to cut them)
  - paper: "James Lighthill, Artificial Intelligence: A General Survey, in Artificial Intelligence: a paper symposium, Science Research Council, London, 1973"
    locator: Part I, the discussion of the combinatorial explosion
---

Combinatorial explosion is the rapid growth of the number of combinations, such as subsets, orders or assignments, when the size of the input grows. The number usually grows exponentially, as $2^n$ or $d^n$, or faster, as $n!$. So a [search space](/search-space/) that a computer lists in a second for one input size takes years when the input is a few dozen items larger. It is the reason that plain [brute-force search](/brute-force-search/) works only for small inputs, and it is the problem that pruning, dynamic programming and [exact exponential algorithms](/exact-exponential-algorithms/) try to control.

## In plain words

Suppose each of ten switches can be on or off. There are about a thousand settings. With twenty switches there are about a million, and with forty there are about a million million. Each new switch doubles the count. Orders grow even faster: ten people can stand in a line in more than three million ways, and twenty people in more ways than a computer can list in decades.

A faster computer helps very little. If a machine is a thousand times faster, it can test only about ten more switches in the same time. This is why programs that try every possibility break down at a size that seems small. The way out is to avoid most of the possibilities: throw away whole groups of them at once, or reuse work that two groups share.

## The idea

**The product rule.** If a candidate is a sequence of $n$ independent choices with $d$ options each, there are $d^n$ candidates. Subsets of an $n$-set are the case $d = 2$, so there are $2^n$ of them. Orders of $n$ items have $n, n-1, \ldots, 1$ options in turn, so there are $n!$ of them. By [Stirling's approximation](/stirling-approximation/),

$$n! = \sqrt{2 \pi n} \left(\frac{n}{e}\right)^n (1 + O(1/n)),$$

so $n!$ grows faster than $c^n$ for each constant $c$, and $\lg n! = n \lg n - n \lg e + O(\log n)$.

**Growth against a fixed budget.** Take a machine that tests $10^9$ candidates per second.

| $n$ | $n^3$ | $2^n$ | $n!$ | time for $2^n$ tests | time for $n!$ tests |
|---|---|---|---|---|---|
| 10 | 1,000 | 1,024 | $3.63 \times 10^{6}$ | 1 microsecond | 3.6 milliseconds |
| 20 | 8,000 | $1.05 \times 10^{6}$ | $2.43 \times 10^{18}$ | 1 millisecond | 77 years |
| 40 | 64,000 | $1.10 \times 10^{12}$ | $8.16 \times 10^{47}$ | 18 minutes | $2.6 \times 10^{31}$ years |
| 60 | 216,000 | $1.15 \times 10^{18}$ | $8.32 \times 10^{81}$ | 37 years | $2.6 \times 10^{65}$ years |

The cubic column stays small. The exponential columns cross from "instant" to "never" within a few tens of items.

**Faster machines.** Let $N$ be the largest input that a method solves within a fixed time. Make the machine $s$ times faster. For a method with $n^b$ steps, the new limit $N'$ satisfies $N'^b = s N^b$, so $N' = s^{1/b} N$: the limit is multiplied by a constant. For a method with $2^n$ steps, $2^{N'} = s \cdot 2^N$, so $N' = N + \lg s$: the limit only moves by a constant. With $s = 1000$, an $n^2$ method handles about 31.6 times larger inputs, an $n^3$ method 10 times larger, and a $2^n$ method only about 10 more items. Garey and Johnson give this comparison in Chapter 1 of their book.

**Where the explosion is real.** The size of a space is an upper bound on the work of exhaustive search, not a lower bound on the problem. Some problems with a huge space are easy: there are $n!$ orders of $n$ numbers, but [merge sort](/merge-sort/) sorts them with $O(n \log n)$ comparisons. Here the $n!$ orders give only a lower bound: a comparison sort needs at least $\lg n!$ comparisons in the worst case. For [NP-complete](/np-complete/) problems no method is known that avoids exponential time in the worst case, and the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) says that for some problems none exists with a much smaller base.

**How to fight it.**

- **Prune.** Test partial candidates and drop each one that cannot be completed, with all its extensions. This is [search tree pruning](/search-tree-pruning/) in [backtracking](/generic-backtracking-algorithm/), and bounding in [branch and bound](/depth-first-branch-and-bound/).
- **Share.** Many branches of a search reach the same subproblem. [Memoization](/memoization/) and dynamic programming solve each subproblem once. The [Held-Karp algorithm](/held-karp-algorithm/) solves the traveling salesman problem in $O(n^2 2^n)$ time instead of the $(n-1)!/2$ tours of brute force.
- **Split.** [Meet in the middle](/horowitz-sahni-algorithm/) searches two halves of size $2^{n/2}$ and joins them, instead of one space of size $2^n$.
- **Remove symmetry.** Keep one candidate of each class of equivalent candidates, as in [symmetry breaking](/symmetry-breaking/).
- **Change the goal.** Accept an approximate answer, restrict the input class, or measure the cost by a small parameter as in [fixed-parameter tractable](/fixed-parameter-tractable/) algorithms.

## Examples

**Traveling salesman.** On $n$ cities there are $(n-1)!/2$ distinct tours for $n \ge 3$. For 10 cities this is 181,440, and a laptop checks them in well under a second. For 20 cities it is $6.08 \times 10^{16}$, and for 30 cities $4.42 \times 10^{30}$.

**Rubik's cube.** The positions that the moves of the cube can reach number

$$\frac{8! \cdot 3^8 \cdot 12! \cdot 2^{12}}{12} = 43{,}252{,}003{,}274{,}489{,}856{,}000 \approx 4.3 \times 10^{19}.$$

The factor $8! \cdot 3^8 \cdot 12! \cdot 2^{12}$ counts all arrangements of the corner and edge pieces. The division by 12 comes from three constraints that the moves keep: the total twist of the corners, the total flip of the edges and the parity of the permutation. A search over all positions at $10^9$ per second takes more than a thousand years.

**Model checking.** A system of $k$ components with $s$ states each has up to $s^k$ global states. In verification this is called the *state explosion*, and it is the main obstacle of exhaustive model checking.

**A non-example.** Shortest paths in a graph: the number of simple paths between two vertices can be exponential, but [Dijkstra's algorithm](/dijkstra/) finds a shortest one in polynomial time, because the best path to each vertex extends a best path to a vertex before it. A large space does not by itself mean a hard problem.

## Where it is used

- **Analysis of exhaustive methods.** The size of the [search space](/search-space/) gives the cost of [brute-force search](/brute-force-search/) and of [generate and test](/generate-and-test/), and the explosion of that size sets the largest input they can handle.
- **The theory of intractability.** The gap between polynomial and exponential growth is the reason that [polynomial time](/polynomial-time/) is the usual line between tractable and intractable problems.
- **Exact exponential algorithms.** The field of [exact exponential algorithms](/exact-exponential-algorithms/) lowers the base of the explosion, for example from $2^n$ to $1.3803^n$ for maximum independent set by simple branching.
- **History of artificial intelligence.** The Lighthill report of 1973 to the British Science Research Council named the combinatorial explosion as a main reason that early search programs did not scale from toy problems to real ones.

## References
