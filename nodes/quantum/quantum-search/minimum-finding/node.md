---
tag: HQ9HF6
kind: problem
slug: minimum-finding
name: Quantum minimum finding
aliases:
- quantum minimum search
- threshold search
area: quantum/quantum-search
level: core
summary: Find the index of a smallest value among N values that are given by an oracle. A quantum computer needs Θ(√N) queries with bounded error, against Θ(N) classically.
prereqs: [unstructured-search, minimum-and-maximum-finding]
see_also: [durr-hoyer-minimum-finding, grover-adaptive-search, find-maximum, max-finding-lower-bound, grover-optimality, selection-problem, minimum-spanning-tree, bbht-search]
sources:
  - paper: arxiv:quant-ph/9607014
    title: Christoph Dürr and Peter Høyer, A quantum algorithm for finding the minimum, arXiv:quant-ph/9607014, 1996
    locator: the problem statement (a table T[0..N-1] of values, find an index y with T[y] minimal) and Theorem 1 (O(sqrt(N)) queries with probability at least 1/2)
  - paper: doi:10.1137/050644719
    title: "Christoph Dürr, Mark Heiligman, Peter Høyer and Mehdi Mhalla, Quantum query complexity of some graph problems, SIAM Journal on Computing 35(6), 2006, pages 1310-1328 (arXiv:quant-ph/0401091)"
    locator: "Section 3 (Theorem 3 on minimum finding, Problem 1 and Theorem 6 on the d smallest values with O(sqrt(dN)) queries, and the remark on the results of Nayak and Wu and of Nayak on the d-th smallest value), Section 4 (Theorem 8, minimum spanning tree) and Section 8 (the lower bound Omega(sqrt(dN)))"
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 4 (search with an unknown number of solutions, the subroutine of the known quantum algorithms) and Section 7 (the lower bound for search)
---

Quantum minimum finding is the problem of finding an index $y$ with $T[y] = \min_j T[j]$, for a table $T[0], \ldots, T[N-1]$ of values from an ordered set that is given only as an oracle. The cost is the number of oracle queries. This page is the problem; the standard algorithm for it is [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/), which uses $O(\sqrt N)$ queries and finds a minimum with probability at least $1/2$. Classically the problem needs $N - 1$ comparisons, as for [finding the minimum and maximum](/minimum-and-maximum-finding/), and $\Omega(N)$ queries even with randomness.

## In plain words

You have a long list of numbers that you cannot see at once. You can only ask about the numbers, one question at a time, and you want the place of the smallest number. A normal computer must look at every number, because the smallest one can be anywhere.

A quantum computer can ask about many places at once. It can find a place whose number is smaller than a given number, and it needs only about the square root of the list length for that. Each time it finds a smaller number, the target gets harder to beat, so it uses this new number as the next target. The total work stays about the square root of the length of the list.

## Definition

**Input.** A number $N$ and a table $T : \{0, 1, \ldots, N-1\} \to V$, where $V$ is a totally ordered set. The table is given as an oracle of one of two kinds:

- *Value oracle.* $|j\rangle|z\rangle \mapsto |j\rangle|z \oplus T[j]\rangle$, for values coded as bit strings.
- *Comparison oracle.* For a fixed index $y$, $|j\rangle|b\rangle \mapsto |j\rangle|b \oplus [T[j] < T[y]]\rangle$. Each call counts as one query, and a call for a new $y$ needs a new oracle.

Two calls of a value oracle, to compute $T[j]$ and to erase it, and a reversible comparison give one call of a comparison oracle. So the two models differ by at most a constant factor.

**Output.** An index $y$ with $T[y] \le T[j]$ for all $j$. If several entries hold the minimum value, any of them is a correct output.

**Cost.** The number of queries, in the [quantum query model](/quantum-query-model/). A quantum algorithm may fail with probability at most a constant, such as $1/2$; repetition lowers it.

## Variants

- **Maximum finding.** Find an index of a largest value. Reverse the order.
- **The $d$ smallest values.** Find a set $I$ of $d$ indices such that no index outside $I$ has a smaller value than one inside $I$.
- **The $d$-th smallest value.** The quantum form of the [selection problem](/selection-problem/). For $d = \lceil N/2 \rceil$ it is the median.
- **Decision version.** Given a value $c$, decide whether some $T[j] < c$. This is [unstructured search](/unstructured-search/) for the marking $f(j) = [T[j] < c]$.
- **Optimization of a function.** $T[x] = F(x)$ for a cost function $F$ on bit strings $x$, given as a reversible circuit. This is the form used for [combinatorial optimization](/combinatorial-optimization-problem/) on quantum computers.
- **Minimum with a given type.** Dürr, Heiligman, Høyer and Mhalla add a second function $g$ and ask for the smallest values of $d$ different types. Graph problems such as the [minimum spanning tree](/minimum-spanning-tree/) reduce to this form.

## Examples

**A table of eight values.** $T = (7, 3, 9, 3, 5, 1, 8, 6)$ with $N = 8$. The minimum is 1, and the only correct output is $y = 5$. For $T' = (4, 2, 6, 2)$, both $y = 1$ and $y = 3$ are correct.

**A cost function.** Let $F(x)$ be the number of edges that the cut $x$ of a graph on $n$ vertices does not cut. Then $N = 2^n$, and an index of the minimum is a [maximum cut](/maximum-cut/). An oracle for $F$ is a reversible circuit that adds up the edges.

**A distance table.** $T[j]$ is the distance from a query point to the $j$-th point of a data set. A minimum index is a nearest neighbour, as in [nearest neighbour search](/nearest-neighbor-search/) without an index structure.

## Known algorithms

| algorithm | queries | success | notes |
|---|---|---|---|
| linear scan | $N - 1$ comparisons | certain | classical, optimal for deterministic comparisons; see [finding the maximum](/find-maximum/) |
| random sampling | $s$ queries | $s/N$ | classical, finds the minimum only if it samples it |
| [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/) | a budget of $22.5\sqrt N + 1.4\log_2^2 N$ Grover iterations | at least $1/2$ | repeated [BBHT search](/bbht-search/) for an entry below the current best; $O(\sqrt N)$ expected queries until the minimum is found |
| Dürr, Heiligman, Høyer and Mhalla | $O(\sqrt{dN})$ | at least $1/2$ | the $d$ smallest values, also of different types |
| [Grover adaptive search](/grover-adaptive-search/) | not bounded in general | heuristic | the same loop for cost functions such as QUBO objectives |

## Bounds

| question | classical | quantum (bounded error) |
|---|---|---|
| index of the minimum, deterministic comparisons | $N - 1$ | not applicable |
| index of the minimum, randomized | $\Theta(N)$ | $\Theta(\sqrt N)$ |
| the $d$ smallest values | $\Theta(N)$ | $\Theta(\sqrt{dN})$ |
| is some $T[j] < c$? | $\Theta(N)$ | $\Theta(\sqrt N)$ |

The deterministic bound $N - 1$ is the [maximum finding lower bound](/max-finding-lower-bound/). The quantum lower bound $\Omega(\sqrt N)$ follows from the reduction below and the [optimality of Grover's search](/grover-optimality/); the Dürr-Høyer algorithm meets it up to a constant. The bound $\Theta(\sqrt{dN})$ for the $d$ smallest values is Theorem 6 and Section 8 of Dürr, Heiligman, Høyer and Mhalla. They also report that Nayak and Wu, and then Nayak, find the $d$-th smallest value with $O(\sqrt{dN})$ queries, which matches the lower bound of Nayak and Wu; so the median needs $\Theta(N)$ queries and has no quantum speedup.

## Reductions

- **Search to minimum finding.** Given $f : \{0, \ldots, N-1\} \to \{0, 1\}$, let $T[x] = 1 - f(x)$. A minimum index $y$ has $f(y) = 1$ if any marked item exists, and one more query checks $f(y)$. So an algorithm for minimum finding with $Q$ queries gives a search algorithm with $Q + 1$ queries, and minimum finding needs $\Omega(\sqrt N)$ quantum and $\Omega(N)$ classical queries.
- **Minimum finding to search.** With a threshold value $c = T[y]$, a search for $j$ with $T[j] < c$ either improves $y$ or shows that $y$ is a minimum. If each search returns a uniformly random improvement, the $r$-th smallest value becomes the threshold with probability $1/r$, so the expected number of thresholds is at most the harmonic number $H_N \le \ln N + 1$.
- **Maximum to minimum.** Reverse the order of $V$.
- **Minimum spanning tree to minimum finding.** Each phase of [Borůvka's algorithm](/boruvka/) needs the lightest edge out of each tree. Dürr, Heiligman, Høyer and Mhalla find these edges as the smallest values of different types and get $O(\sqrt{nm})$ queries for a graph with $n$ vertices and $m$ edges in the array model (their Theorem 8).

## Applications

- **Graph algorithms.** The quantum algorithms of Dürr, Heiligman, Høyer and Mhalla for the minimum spanning tree and for [single-source shortest paths](/single-source-shortest-paths/) use minimum finding as the main step.
- **Optimization.** Finding the minimum of a cost function over $2^n$ bit strings with $O(2^{n/2})$ evaluations, a quadratic speedup over exhaustive search. Grover adaptive search is the practical form.
- **Nearest neighbours and clustering.** The closest of $N$ stored points to a query point, with $O(\sqrt N)$ distance evaluations.
- **A subroutine.** Many quantum algorithms for problems on tables and graphs call minimum or maximum finding inside a larger loop.

## References
