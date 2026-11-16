---
tag: SJ06Z3
kind: concept
slug: parameterized-counting-complexity
name: Parameterized counting complexity
aliases:
- '#W[1]'
- para-#P
area: complexity/parameterized-complexity
level: research
summary: "The study of counting versions of parameterized problems. Counting k-cliques is #W[1]-complete, and counting k-paths or k-matchings is #W[1]-hard although the decision versions are easy."
prereqs: [w-hierarchy, parameterized-reduction, parsimonious-reduction]
see_also: [k-path-color-coding, counting-fixed-length-paths, parameterized-longest-path, parsimonious-reduction, turing-reduction, permanent-computation, model-counting, fpras]
sources:
  - book: isbn:9783540299523
    title: "Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006"
    locator: "Chapter 14, Parameterized Counting Problems, pp. 357-388"
  - paper: doi:10.1137/S0097539703427203
    title: "Jörg Flum and Martin Grohe, The parameterized complexity of counting problems, SIAM Journal on Computing 33(4), 892-922 (2004)"
    locator: "the classes #W[t], #W[1]-completeness of counting cliques, and #W[1]-completeness of counting paths and cycles of length k under fpt Turing reductions"
  - paper: doi:10.1016/j.apal.2005.06.010
    title: "Catherine McCartin, Parameterized counting problems, Annals of Pure and Applied Logic 138(1-3), 147-182 (2006)"
    locator: "an independent definition of the #W hierarchy and of parsimonious parameterized reductions"
  - paper: doi:10.1007/978-3-642-39206-1_30
    title: "Radu Curticapean, Counting matchings of size k is #W[1]-hard, ICALP 2013, LNCS 7965, 352-363"
    locator: "#W[1]-hardness of counting matchings with k edges"
  - paper: "Radu Curticapean and Dániel Marx, Complexity of counting subgraphs: only the boundedness of the vertex-cover number counts, FOCS 2014"
    locator: the dichotomy for counting copies of a pattern graph from a fixed class
---

Parameterized counting complexity asks how hard it is to count the solutions of a [parameterized problem](/parameterized-problem/), not only to decide whether one exists. Its main class is #W[1], the counting form of [W[1]](/w-hierarchy/), and counting the cliques of size $k$ is complete for it. The theory shows that counting can be hard when deciding is easy: whether a graph has a path with $k$ vertices can be decided in FPT time by [color coding](/k-path-color-coding/), but counting these paths is #W[1]-complete. Para-#P is the counting form of para-NP, for problems that are hard for one fixed value of the parameter.

## In plain words

Some questions ask if a small pattern occurs in a large network, for example a chain of ten people where each knows the next. Other questions ask how many times it occurs. The second kind looks only a little harder, but it can be much harder.

For a chain, a clever random method finds one fast when the chain is short, even in a very large network. No method of this kind is known that gives the exact number of chains, and the theory gives strong reasons to believe that none exists. The same happens for sets of separate pairs: finding many separate pairs is easy, but counting the sets of exactly ten pairs is hard.

The theory also tells which patterns are easy to count. A pattern is easy when a few of its points touch all of its lines, as in a star.

## The idea

**Counting problems.** A parameterized counting problem is a function $F$ that maps an input $(x, k)$ to a natural number, usually the number of solutions of size $k$. For example, p-#Clique maps $(G, k)$ to the number of cliques with $k$ vertices in $G$. $F$ is *fixed-parameter tractable* if an algorithm computes $F(x, k)$ in time $f(k) \cdot |x|^{O(1)}$ for a computable $f$. If the counting problem is FPT, then so is the decision problem, since a solution exists exactly when the count is positive.

**Reductions.** There are two kinds, both computed in time $f(k) \cdot |x|^{O(1)}$:

- an *fpt parsimonious reduction* from $F$ to $F'$ maps $(x, k)$ to $(x', k')$ with $k' \le g(k)$ and $F(x, k) = F'(x', k')$, like a [parsimonious reduction](/parsimonious-reduction/) in classical counting;
- an *fpt Turing reduction* computes $F(x, k)$ with an oracle for $F'$, and asks only queries $(y, \ell)$ with $\ell \le g(k)$, like a [Turing reduction](/turing-reduction/).

FPT is closed under both, because a query with $\ell \le g(k)$ costs at most $f'(g(k)) \cdot |y|^{O(1)}$, and $|y|$ is at most the running time of the reduction.

**The #W hierarchy.** Flum and Grohe (2004) define $\#\mathsf{W}[t]$ as the class of counting problems with an fpt parsimonious reduction to counting the satisfying assignments of weight $k$ of circuits of constant depth and [weft](/w-hierarchy/) at most $t$. This is the counting version of the definition of $\mathsf{W}[t]$ by [weighted satisfiability](/weighted-satisfiability/). McCartin (2006) gave an equivalent definition independently. The standard reductions for W[1]-completeness of clique can be made parsimonious, and Flum and Grohe prove that p-#Clique is #W[1]-complete under fpt parsimonious reductions.

**What #W[1]-hardness means.** Suppose that $F$ is #W[1]-hard under fpt Turing reductions and $F$ is FPT. Then p-#Clique is FPT, because FPT is closed under the reduction. Then p-Clique is FPT, because a clique exists exactly when the count is positive. So $\mathsf{FPT} = \mathsf{W}[1]$. The usual assumption that [FPT and W[1] are different](/fpt-w1-conjecture/) is therefore enough to show that a #W[1]-hard problem is not FPT.

**Counting is harder than deciding.** These results show the gap:

- *Paths and cycles.* Deciding whether a graph has a path with $k$ vertices, or a cycle of length $k$, is FPT by color coding. Flum and Grohe (2004) prove that counting these paths and these cycles is #W[1]-complete under fpt Turing reductions. Color coding gives a randomized approximate count in FPT time, but not an exact count. See [parameterized longest path](/parameterized-longest-path/).
- *Matchings.* Deciding whether a graph has a matching with $k$ edges takes polynomial time, by a [maximum matching](/maximum-matching/) algorithm. Curticapean (2013) proved that counting the matchings with exactly $k$ edges is #W[1]-hard. Counting all [perfect matchings](/perfect-matching/) is classically #P-complete, as the [permanent](/permanent-computation/) is, but this is a different statement, because there $k = n/2$ grows with the input.

**The subgraph dichotomy.** Fix a class $\mathcal{H}$ of pattern graphs, and count the copies of a pattern $H \in \mathcal{H}$ in a graph $G$, with parameter $|V(H)|$. Curticapean and Marx (2014) proved that if the patterns in $\mathcal{H}$ have bounded vertex cover number, the problem is solvable in polynomial time, and otherwise it is #W[1]-complete. Paths, cycles and matchings have unbounded vertex cover number, since a matching with $k$ edges needs $k$ vertices to cover it. Stars have vertex cover number 1.

**Para-#P.** In the same way as para-NP is NP after a precomputation on the parameter, para-#P is #P after a precomputation on the parameter. If one slice of a counting problem is #P-hard, the problem is not FPT unless every #P function is computable in polynomial time. In the classical setting, counting is very strong: by [Toda's theorem](/toda-theorem/), every problem in the polynomial hierarchy is decided in polynomial time with a #P oracle.

## Examples

All examples use the Petersen graph, which has 10 vertices, 15 edges, and degree 3 at every vertex.

**Paths.** The numbers of paths with $1, 2, \ldots, 10$ vertices are

| vertices | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| paths | 10 | 15 | 30 | 60 | 120 | 180 | 240 | 300 | 300 | 120 |

So the decision answer for a path with $k$ vertices is yes for every $k \le 10$, and the counts carry much more information. For cycles, the counts by length are 12 for length 5, 10 for length 6, 15 for length 8 and 20 for length 9, and 0 for lengths 3, 4, 7 and 10. The 120 paths with 10 vertices are Hamiltonian paths, but there is no Hamiltonian cycle.

**Matchings.** The numbers of matchings with $1, 2, 3, 4, 5$ edges are 15, 75, 145, 90 and 6. A maximum matching has 5 edges and a polynomial-time algorithm finds one, so every decision question here is easy. Counting the matchings with exactly $k$ edges is the #W[1]-hard problem of Curticapean.

**Stars.** A star with $k$ edges has vertex cover number 1, so it is easy to count. Each copy has one center $v$ and $k$ of its neighbors, so the number of copies is $\sum_{v} \binom{\deg v}{k}$ for $k \ge 2$. In the Petersen graph this is $10 \cdot \binom{3}{2} = 30$ for $k = 2$, which agrees with the 30 paths with 3 vertices above, and $10 \cdot \binom{3}{3} = 10$ for $k = 3$.

**Colorings.** Counting the proper colorings with $q$ colors, with parameter $q$, is para-#P-hard, because the slice $q = 3$ is #P-complete. The Petersen graph has 0 proper colorings with 2 colors, 120 with 3 colors and 12960 with 4 colors.

## Where it is used

- *Subgraph counts in networks.* Network analysis counts small patterns, such as paths and cycles, in large graphs. The dichotomy explains why exact counts are fast for star-like patterns and are not expected to be FPT for long paths, so practical tools use approximate counts or small patterns.
- *Approximate counting.* Because exact counting of $k$-paths is #W[1]-hard, research asks for [randomized approximation schemes](/fpras/) in FPT time. Color coding gives one for $k$-paths, and [counting walks of fixed length](/counting-fixed-length-paths/) by matrix powers is easy because walks may repeat vertices.
- *Model counting.* [Model counting](/model-counting/) of CNF formulas is #P-complete in general. With the treewidth of the formula as the parameter, it is FPT by dynamic programming over a tree decomposition.
- *Lower bounds.* A #W[1]-hardness proof gives a statement "not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$" for a counting problem, in the same way as [W[1]-hardness](/w-hardness/) does for a decision problem.

## References
