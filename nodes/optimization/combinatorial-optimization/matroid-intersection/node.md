---
tag: M7BWC7
kind: problem
slug: matroid-intersection
name: Matroid intersection
aliases:
- maximum common independent set
- matroid intersection problem
- two-matroid intersection
area: optimization/combinatorial-optimization
level: advanced
summary: Find a largest set independent in two matroids simultaneously.
prereqs: [matroid, partition-matroid, graphic-matroid, combinatorial-optimization-problem]
see_also: [matroid-intersection-algorithm, matroid-intersection-theorem, rado-edmonds-theorem, bipartite-matching, arborescence, three-dimensional-matching, submodular-minimization, matroid-greedy-algorithm]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 41, Matroid intersection; the weighted problem is in the chapter that follows it
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 13, Matroids (the sections on matroid intersection and weighted matroid intersection)
  - paper: "Jack Edmonds, Submodular functions, matroids, and certain polyhedra, in Combinatorial Structures and Their Applications (Proceedings of the Calgary International Conference, 1969), Gordon and Breach, 1970, 69 to 87"
    locator: the min-max theorem and the polytope of common independent sets
  - paper: doi:10.1007/BF01681329
    title: Eugene L. Lawler, Matroid intersection algorithms, Mathematical Programming 9, 31 to 56, 1975
    locator: the cardinality and weighted algorithms
  - paper: doi:10.1137/0215066
    title: William H. Cunningham, Improved bounds for matroid partition and intersection algorithms, SIAM Journal on Computing 15(4), 948 to 957, 1986
    locator: the bound of O(n r^1.5) independence oracle calls
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Appendix A3.1, problem SP1, three-dimensional matching
---

Matroid intersection asks for a largest set that is independent in two [matroids](/matroid/) on the same ground set. One matroid alone is easy: the [greedy algorithm](/matroid-greedy-algorithm/) solves it. Two matroids together already contain [bipartite matching](/bipartite-matching/), [arborescences](/arborescence/) and spanning trees with color constraints, and greedy no longer works. The problem is still solvable in polynomial time: with independence oracles, the [matroid intersection algorithm](/matroid-intersection-algorithm/) of Edmonds and Lawler uses $O(n r^2)$ oracle calls, and Cunningham's version uses $O(n r^{1.5})$, where $n$ is the number of elements and $r$ the answer. The weighted version is also polynomial. The optimum has the min-max characterization of the [matroid intersection theorem](/matroid-intersection-theorem/). For three matroids the problem is [NP-hard](/np-hard/), since it contains [three-dimensional matching](/three-dimensional-matching/).

## In plain words

You choose items under two sets of rules. Each set of rules has the matroid property: if you are allowed a small group and a bigger group, you can always add something from the bigger group to the small one. For one set of rules, picking items one by one never goes wrong. For two sets of rules at once, it can. For example, you may want links between towns without a loop, and at most one link from each company.

The task is to choose as many items as possible that both sets of rules allow. A smart method finds the best choice quickly by trading items. Adding a third set of rules makes the task very hard.

## Definition

**Input.** A finite ground set $E$ with $n = |E|$, and two matroids $M_1 = (E, \mathcal{I}_1)$ and $M_2 = (E, \mathcal{I}_2)$. In the general model each matroid is given by an *independence oracle* that answers whether a set $S \subseteq E$ is in $\mathcal{I}_i$. Concrete matroids, such as [graphic](/graphic-matroid/), [partition](/partition-matroid/) and [linear](/linear-matroid/) matroids, can be given explicitly, and then each oracle call takes polynomial time.

**Output.** A set $I \in \mathcal{I}_1 \cap \mathcal{I}_2$ (a *common independent set*) of largest size.

**Value.** By the [matroid intersection theorem](/matroid-intersection-theorem/),
$$\max \{|I| : I \in \mathcal{I}_1 \cap \mathcal{I}_2\} = \min_{U \subseteq E} \bigl( r_1(U) + r_2(E \setminus U) \bigr),$$
where $r_1$ and $r_2$ are the rank functions. A set $U$ that attains the minimum certifies optimality.

**Decision version.** Given also $k$, is there a common independent set of size at least $k$? Both a set $I$ and a set $U$ are certificates that can be checked with $O(n)$ oracle calls, so the decision problem is in NP ∩ coNP even before one knows an algorithm.

## Variants

- **Weighted matroid intersection.** Each element has a weight $w(e)$, and the task is a common independent set of largest weight, or a common basis of least weight. It is polynomial: Edmonds (1970) and Lawler (1975) gave primal-dual algorithms, and Frank (1981) a weight-splitting algorithm. The polytope $\{x \ge 0 : x(S) \le r_i(S) \text{ for all } S \subseteq E, \; i = 1, 2\}$ is integral (Edmonds 1970), so linear programming also gives the answer.
- **Common basis.** Decide whether the two matroids have a common basis. This is the case where the maximum equals $r_1(E) = r_2(E)$.
- **$k$ matroids, $k \ge 3$.** NP-hard. The greedy method, which adds an element whenever all matroids allow it, gives a set of size at least $1/k$ of the optimum. Local search gives a ratio near $k/2$ (Lee, Sviridenko and Vondrák, 2010).
- **Matroid union and partition.** Find the largest set that is a union of $k$ independent sets, one from each of $k$ matroids. It reduces to matroid intersection and has its own direct algorithm.
- **Matroid parity (matching).** The elements come in pairs, and a set must take both or neither element of each pair. It contains general graph matching. Lovász (1980) solved it in polynomial time for linear matroids, but for matroids given by oracles it needs exponentially many oracle calls in the worst case (Lovász 1980; Jensen and Korte 1982).

## Examples

**Colorful forest.** Six links between towns 1 to 5 are offered by four companies:

| link | $a$ = 1-5 | $b$ = 2-5 | $c$ = 3-4 | $d$ = 1-2 | $e$ = 2-5 | $f$ = 1-4 |
| --- | --- | --- | --- | --- | --- | --- |
| company | red | yellow | yellow | green | blue | yellow |

$M_1$ is the graphic matroid (no cycles) and $M_2$ the partition matroid with at most one link per company. The set $\{a, c, d\}$ is common independent. Each matroid alone has rank 4, but the maximum common independent set has size 3. The set $U = \{a, d, e\}$ proves this: $r_1(U) = 2$ because its links lie on the three towns 1, 2 and 5, and $r_2(\{b, c, f\}) = 1$ because those links are all yellow. Greedy in the order $a, b, \ldots, f$ takes $a$ and $b$ and then stops at a maximal set of size 2.

**Bipartite matching.** For a bipartite graph with sides $L$ and $R$, take as $M_1$ the partition matroid on the edges with at most one edge at each vertex of $L$, and as $M_2$ the same for $R$. Common independent sets are exactly the matchings.

**Arborescence.** In a directed graph with root $s$, the spanning arborescences rooted at $s$ are the common independent sets of size $|V| - 1$ of the graphic matroid of the underlying undirected graph and the partition matroid that allows at most one arc into each vertex and no arc into $s$.

## Known algorithms

| method | oracle calls or time | notes |
| --- | --- | --- |
| [Augmenting paths](/matroid-intersection-algorithm/) (Edmonds 1970, Lawler 1975) | $O(n r^2)$ independence oracle calls | exact, gives the certificate $U$ |
| Shortest paths in phases (Cunningham 1986) | $O(n r^{1.5})$ independence oracle calls | the analogue of [Hopcroft-Karp](/hopcroft-karp/) |
| Weighted: primal-dual or weight splitting (Lawler 1975, Frank 1981) | polynomial in $n$ and the oracle time | for weights; finds a heaviest common independent set of each size |
| Linear matroids, algebraic (Harvey 2009) | $O(n r^{\omega - 1})$ field operations | by matrix multiplication with exponent $\omega$ |
| Greedy | $O(n)$ oracle calls | only a maximal set, at least half the optimum |

For special cases, such as bipartite matching or arborescences, the specialized algorithms ([Hopcroft-Karp](/hopcroft-karp/), [Edmonds' arborescence algorithm](/edmonds-arborescence/)) are faster. Work since 2019, for example by Chakrabarty, Lee, Sidford, Singla and Wong, has reduced the number of oracle calls for general matroids further, in particular with rank oracles.

## Bounds

- **Upper bound.** $O(n r^{1.5})$ independence oracle calls (Cunningham 1986), with polynomial extra time.
- **Approximation by greedy.** Any maximal common independent set has at least half the size of a maximum one. Let $G$ be maximal and $O$ optimal. Each element of $O$ lies in the span of $G$ in $M_1$ or in $M_2$, because otherwise it could be added to $G$. The elements of $O$ in the span of $G$ in $M_1$ form an independent set in a set of rank $|G|$, so there are at most $|G|$ of them, and the same holds for $M_2$. So $|O| \le 2|G|$. The ratio 2 is tight, already for bipartite matching on a path with three edges.
- **Integrality.** The linear programming relaxation over the intersection of the two matroid polytopes has no gap (Edmonds 1970).
- **Three matroids.** NP-hard to solve exactly. For $k$-dimensional matching, which is a special case with $k$ partition matroids, approximation within a factor $O(k / \log k)$ of the optimum is NP-hard (Hazan, Safra and Schwartz, 2006).

## Reductions

- **Bipartite matching to matroid intersection**, with two partition matroids, as above.
- **Spanning arborescence to matroid intersection.** In a directed graph with root $s$, an arborescence rooted at $s$ is a common basis of size $|V| - 1$ of the graphic matroid of the underlying undirected graph and the partition matroid that allows at most one arc into each vertex and none into $s$.
- **Matroid union to matroid intersection.** Take the direct sum of $k$ copies of the matroids, and intersect it with the partition matroid that allows each original element at most once.
- **Three-dimensional matching to three matroids.** The triples are the elements, and each of the three coordinates gives a partition matroid with capacity 1. [Three-dimensional matching](/three-dimensional-matching/) is NP-complete (Garey and Johnson, problem SP1), so matroid intersection for three matroids is NP-hard.
- **Directed Hamiltonian path to three matroids.** A set of $|V| - 1$ arcs is a [Hamiltonian path](/hamiltonian-path/) exactly when it is a forest in the undirected sense, enters each vertex at most once and leaves each vertex at most once: a graphic matroid and two partition matroids.
- **Matroid intersection to submodular minimization.** The value $\min_U \bigl(r_1(U) + r_2(E \setminus U)\bigr)$ is the minimum of a [submodular function](/submodular-function/), so [submodular minimization](/submodular-minimization/) computes the optimum value.

## Applications

- **Matching and assignment.** Bipartite matching, and assignment with an extra independence constraint, such as Rado's independent transversals.
- **Network design.** Spanning trees or forests with at most a given number of edges of each color, type or owner, and [arborescences](/arborescence/) with degree or type rules.
- **Packing and covering.** Through matroid union: edge-disjoint spanning trees, covering a graph with the fewest forests (arboricity), and rigidity tests based on counts of edges.
- **Linear algebra.** Choose linearly independent vectors, at most one from each group, as in the selection of measurements or the structural rank of a matrix with free parameters.
- **Theory.** A standard example of a problem with a min-max theorem and a polynomial-time algorithm that is not a flow problem. Many results on submodular optimization extend it.

## References
