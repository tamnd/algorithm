---
tag: T636NY
kind: problem
slug: traveling-salesman-decision
name: Traveling salesman decision problem
aliases:
- TSP decision
- TSP (decision version)
area: complexity/reductions-catalogue
level: core
summary: Given distances between n cities and a bound k, decide whether a tour visiting every city once has total length at most k. NP-complete, even with distances 1 and 2.
prereqs: [traveling-salesman-problem, hamiltonian-cycle-np-completeness, np-complete]
see_also: [hamiltonian-cycle-problem, metric-tsp, euclidean-tsp, held-karp-algorithm, christofides-algorithm, general-tsp-inapproximability, strong-np-hardness, zero-one-equations]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A2.3, problem ND22 (Traveling salesman), with its comments on distances 1 and 2 and on Euclidean distances
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 34.5.4 (the traveling-salesman problem, reduction from HAM-CYCLE)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2006
    locator: Section 8.3, the reduction from RUDRATA CYCLE to TSP and the remark on the triangle inequality and approximation
  - paper: doi:10.1016/0304-3975(77)90012-3
    title: Christos H. Papadimitriou, The Euclidean traveling salesman problem is NP-complete, Theoretical Computer Science 4(3), 1977, pages 237 to 244
    locator: the main theorem
---

The traveling salesman decision problem gives a table of distances between $n$ cities and a bound $k$, and asks whether some tour that visits every city exactly once and returns to the start has total length at most $k$. It is the decision form of the [traveling salesman problem](/traveling-salesman-problem/), and it is [NP-complete](/np-complete/). The proof is a two-line reduction from the [Hamiltonian cycle problem](/hamiltonian-cycle-np-completeness/): roads of the graph get length 1 and all other pairs get length 2. Because the distances are 1 and 2, the problem is NP-complete in the [strong sense](/strong-np-hardness/), and it stays NP-complete with the triangle inequality.

## In plain words

A salesperson must visit every city once and come home, and the trip should be short. The question here is a yes or no version: is there a trip no longer than a given limit?

Checking a proposed trip is easy: add up its legs and compare. But the number of possible trips grows like a factorial. The reason no fast method is known is that the question contains another hard puzzle. Take a road map, and say that a road between two cities costs 1 and that every missing road costs 2. Then a trip of total cost equal to the number of cities exists exactly when there is a round trip that uses only real roads.

## Definition

**Instance.** A number $n \ge 3$ of cities, a symmetric matrix of nonnegative integer distances $d(i, j)$ for $1 \le i < j \le n$, and an integer bound $k$.

**Question.** Is there a permutation $\pi$ of $\{1, \ldots, n\}$ with
$$\sum_{t=1}^{n-1} d(\pi(t), \pi(t+1)) + d(\pi(n), \pi(1)) \le k \;?$$

**Encoding.** The distances and $k$ are written in binary, so the input has about $\binom{n}{2}$ numbers. The certificate is the permutation $\pi$. The verifier checks that it is a permutation and adds $n$ distances, in polynomial time on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions, from Hamiltonian cycle (Garey and Johnson problem ND22; Cormen, Leiserson, Rivest and Stein Section 34.5.4). It is NP-complete in the strong sense, since the reduction uses only the distances 1 and 2.

## Variants

- **Optimization.** Find a shortest tour; see [traveling salesman problem](/traveling-salesman-problem/). Binary search on $k$ finds the optimal length with $O(\log(n \max d))$ calls to the decision problem, and a tour can then be found by testing, one pair at a time, whether raising its distance changes the optimum. So the decision and optimization forms are polynomial-time equivalent.
- **Metric TSP.** The distances satisfy the triangle inequality $d(i, j) \le d(i, l) + d(l, j)$. It is still NP-complete, because the distances 1 and 2 satisfy this inequality. See [metric TSP](/metric-tsp/).
- **Euclidean TSP.** The cities are points in the plane with Euclidean distances. Papadimitriou (1977) proved it NP-hard. With exact distances, membership in NP is open, because no polynomial-time method is known to compare a sum of square roots of integers with an integer. With rounded distances it is NP-complete. See [Euclidean TSP](/euclidean-tsp/).
- **Asymmetric TSP.** $d(i, j)$ and $d(j, i)$ may differ. It contains the symmetric problem, so it is NP-complete too, by a reduction from directed Hamiltonian cycle.
- **Through a graph.** Some books allow only the edges of a given graph $G$. Giving the non-edges a length larger than any tour of edges turns this form into the complete-graph form.

## Examples

A script built the instance from the reduction below for three graphs and computed the optimal tour length with the [Held-Karp algorithm](/held-karp-algorithm/). In each case the bound is $k = n$.

| graph | $n$ | edges | Hamiltonian | optimal tour | answer for $k = n$ |
|---|---|---|---|---|---|
| 5-cycle plus one chord | 5 | 6 | yes | 5 | yes |
| $K_{2,3}$ | 5 | 6 | no | 6 | no |
| Petersen graph | 10 | 15 | no | 11 | no |

- **Forward.** In the 5-cycle $0, 1, 2, 3, 4$ with the chord $0$-$2$, the Hamiltonian cycle $0, 1, 2, 3, 4$ uses five edges, so it maps to a tour of length 5.
- **Backward.** A tour of length 5 on 5 cities must use five legs of length 1, so it uses only edges of the graph and is a Hamiltonian cycle.
- **No-instances.** $K_{2,3}$ is bipartite with sides of size 2 and 3, so it has no Hamiltonian cycle; the best tour uses one leg of length 2. The Petersen graph has no Hamiltonian cycle, and its best tour also uses exactly one non-edge.

On 300 random graphs with 3 to 7 vertices, the script confirmed that the distances satisfy the triangle inequality, and that the optimal tour has length at most $n$ exactly when the graph is Hamiltonian (86 yes-instances and 214 no-instances).

## Known algorithms

- **Brute force.** Try all $(n-1)!/2$ tours.
- **Dynamic programming.** The [Held-Karp algorithm](/held-karp-algorithm/) solves the optimization problem in $O(2^n n^2)$ time and $O(2^n n)$ space.
- **Exact solvers.** Branch and cut with linear programming bounds, such as the [Held-Karp bound](/held-karp-bound/), solves large practical instances; see [traveling salesman problem](/traveling-salesman-problem/).
- **Approximation for metric instances.** The [Christofides algorithm](/christofides-algorithm/) finds a tour at most $3/2$ times the optimum. Euclidean instances have a polynomial-time approximation scheme; see [Euclidean TSP](/euclidean-tsp/).
- **Local search.** [2-opt](/two-opt/) and [Lin-Kernighan](/lin-kernighan/) give good tours in practice, with no worst-case guarantee.

## Bounds

- **NP-completeness.** No polynomial-time algorithm exists unless P = NP. Since the reduction uses only the distances 1 and 2, there is not even a [pseudo-polynomial](/pseudo-polynomial-time/) algorithm unless P = NP.
- **No approximation in general.** Without the triangle inequality, no polynomial-time algorithm approximates the optimum within any factor $\rho \ge 1$ that is computable in polynomial time, unless P = NP; see [general TSP inapproximability](/general-tsp-inapproximability/).
- **Complement.** Deciding that every tour is longer than $k$ is [coNP-complete](/co-np-complete/).

## Reductions

**From Hamiltonian cycle (Karp reduction).** Let $G = (V, E)$ be a graph with $n \ge 3$ vertices.

- *Map.* Use the vertices as cities, with $d(u, v) = 1$ if $\{u, v\} \in E$ and $d(u, v) = 2$ otherwise, and set $k = n$.
- *Cost.* The map writes $\binom{n}{2}$ small numbers, in $O(n^2)$ time.
- *If $G$ has a Hamiltonian cycle, then there is a tour of length at most $n$.* The cycle visits every vertex once, and each of its $n$ legs is an edge of length 1. So as a tour its length is $n$.
- *If there is a tour of length at most $n$, then $G$ has a Hamiltonian cycle.* Take any tour of length at most $n$. It has $n$ legs, each of length at least 1, so every leg has length exactly 1 and is an edge of $G$. A tour visits every vertex exactly once, so the legs form a Hamiltonian cycle of $G$.

The distances 1 and 2 satisfy the triangle inequality, since $d(i, j) \le 2 \le d(i, l) + d(l, j)$. So the same reduction proves metric TSP NP-complete.

**The gap version.** Dasgupta, Papadimitriou and Vazirani note that the non-edges can get length $1 + \alpha$ for any $\alpha > 0$. With $\alpha = 1$ the triangle inequality holds. With a large $\alpha$, a non-Hamiltonian graph has no tour shorter than $n + \alpha$, so an approximation algorithm with ratio below $1 + \alpha / n$ would decide Hamiltonian cycle. This is the proof of [general TSP inapproximability](/general-tsp-inapproximability/).

**Chain from 3-SAT.** In the chain of Dasgupta, Papadimitriou and Vazirani, TSP comes from Rudrata (Hamiltonian) cycle, which comes from [zero-one equations](/zero-one-equations/). The more common chain uses [vertex cover](/vertex-cover/) and the [edge gadget proof](/hamiltonian-cycle-np-completeness/).

## Applications

- **Routing hardness.** Vehicle routing, delivery and drilling problems contain TSP, so their exact versions are NP-hard by this reduction.
- **Source problem.** TSP with distances 1 and 2 is a convenient source for hardness proofs, because it is strongly NP-complete and metric.
- **Benchmark for algorithms.** Because the problem is hard in theory but solvable in practice for large instances, it is a standard test for exact and heuristic methods; see [traveling salesman problem](/traveling-salesman-problem/).

## References
