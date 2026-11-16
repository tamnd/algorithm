---
tag: ZYG5PX
kind: problem
slug: parameterized-clique
name: Parameterized clique
aliases:
- k-clique
area: complexity/parameterized-complexity
level: core
summary: "Decide whether a graph has a clique of size k, with k as the parameter. W[1]-complete, solvable in time n^(omega k/3), and no f(k) n^o(k) algorithm unless ETH fails."
prereqs: [clique-problem, fixed-parameter-tractable]
see_also: [clique-w1-completeness, parameterized-independent-set, maximum-clique, clique-problem, w-hierarchy, triangle-detection-hypothesis, hyperclique-hypothesis, parameterized-inapproximability]
sources:
  - paper: doi:10.1016/0304-3975(94)00097-3
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness II: on completeness for W[1], Theoretical Computer Science 141(1-2), 109-131 (1995)"
    locator: the main theorem, independent set and clique are W[1]-complete
  - paper: "Jaroslav Nešetřil and Svatopluk Poljak, On the complexity of the subgraph problem, Commentationes Mathematicae Universitatis Carolinae 26(2), 1985"
    locator: the reduction of k-clique to triangle detection and fast matrix multiplication
  - paper: doi:10.1016/j.jcss.2006.04.007
    title: "Jianer Chen, Xiuzhen Huang, Iyad A. Kanj and Ge Xia, Strong computational lower bounds via parameterized complexity, Journal of Computer and System Sciences 72(8), 1346-1367 (2006)"
    locator: no f(k) n^o(k) algorithm for clique unless ETH fails
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13 (W[1]-hardness of clique and multicolored clique) and Theorem 14.21 (the ETH lower bound)
---

Parameterized clique, p-Clique, is the [clique problem](/clique-problem/) in its decision form with the clique size $k$ as the [parameter](/parameter/). It is the standard W[1]-complete problem: it has no algorithm in time $f(k) \cdot n^{O(1)}$ unless $\mathsf{FPT} = \mathsf{W}[1]$, and none in time $f(k) \cdot n^{o(k)}$ unless the Exponential Time Hypothesis fails. The best known algorithm, by Nešetřil and Poljak, uses fast matrix multiplication and runs in time $O(n^{\omega k/3})$ when 3 divides $k$. This page gives the parameterized view only; the [clique problem](/clique-problem/) page has the NP-completeness proof, and [maximum clique](/maximum-clique/) has the algorithms for the largest clique.

## In plain words

In a network of people, a clique is a group in which everyone knows everyone else. The question is whether there is such a group of a given small size.

You can check every group of that size. The number of groups grows like the number of people raised to the power of the group size, so even groups of ten are out of reach in a large network. Clique is the main example of a problem where nobody knows a method that keeps the power fixed, and where experts believe that no such method exists. The best known trick, with fast matrix products, only lowers the power to about four-fifths of its value.

## Definition

The input is a graph $G = (V, E)$ with $n = |V|$, given as an adjacency matrix, and a number $k$. A set $S \subseteq V$ is a *clique* if every two vertices of $S$ are adjacent.

**p-CLIQUE**

- Instance: a graph $G = (V, E)$ and an integer $k \ge 0$.
- Parameter: $k$.
- Question: does $G$ have a clique $S$ with $|S| = k$?

A clique of size more than $k$ contains one of size exactly $k$, so "at least $k$" gives the same problem. A yes-instance has a certificate of $k$ vertex names, which is checked in $O(k^2)$ time with the matrix.

**Complexity.** p-Clique is W[1]-complete under [parameterized reductions](/parameterized-reduction/) (Downey and Fellows 1995); the proof is on [clique is W[1]-complete](/clique-w1-completeness/). As a classical problem, with $k$ part of the input, it is NP-complete.

## Variants

- *Multicolored clique.* The vertex set is split into $k$ classes, and the clique must have one vertex in each. It is W[1]-complete as well, by the map $(i, v)$ on [parameterized reduction](/parameterized-reduction/), and it is the usual source problem for W[1]-hardness proofs.
- *Independent set.* A clique in $G$ is an independent set in the [complement graph](/complement-graph/), so [p-Independent-Set](/parameterized-independent-set/) is the same problem with the same parameter.
- *Parameter $n - k$.* $G$ has a clique of size $k$ exactly when the complement has a vertex cover of size $n - k$. With the parameter $n - k$ the problem is [vertex cover](/parameterized-vertex-cover/), which is FPT.
- *Structural parameters.* With the maximum degree $\Delta$, a clique lies in some closed neighborhood $N[v]$ of at most $\Delta + 1$ vertices, and trying all subsets takes time $O(2^{\Delta} \Delta^2 n)$. With the [degeneracy](/degeneracy/) $d$, a clique lies in $\{v\}$ plus the at most $d$ later neighbors of its first vertex in a degeneracy order, which gives time $O(2^d d^2 n)$. Both parameterizations are FPT.
- *Planar graphs.* A [planar graph](/planar-graph/) has no clique of size 5, so the problem is in P on planar graphs for every $k$.
- *Counting.* Counting the cliques of size $k$ is #W[1]-complete; see [parameterized counting complexity](/parameterized-counting-complexity/).
- *Hypergraphs and weights.* The [hyperclique](/hyperclique/) problem asks for $k$ vertices of a hypergraph with all hyperedges among them. Weighted versions ask for a clique of minimum weight or of weight zero; see the [min-weight k-clique hypothesis](/min-weight-k-clique-hypothesis/).

## Examples

The Petersen graph has 10 vertices and 15 edges and no triangle. It has 10 cliques of size 1, 15 of size 2 and none of size 3. So (Petersen, 2) is a yes-instance and (Petersen, 3) is a no-instance.

The house graph is a square 0, 1, 2, 3 with a roof vertex 4 joined to 0 and 1. It has 5, 6, 1 and 0 cliques of sizes 1, 2, 3 and 4. The only triangle is $\{0, 1, 4\}$.

A worked Nešetřil and Poljak step for $k = 6$. Let $G$ have 9 vertices: a complete graph on $\{0, \ldots, 5\}$ and the extra edges 06, 07, 16, 18, 27, 36, 37, 38, 47, 57, 67, 68 and 78, for 28 edges in all. $G$ has exactly two cliques of size 6, $\{0, 1, 2, 3, 4, 5\}$ and $\{0, 2, 3, 4, 5, 7\}$, and no clique of size 7. Build the graph $H$ whose vertices are the 28 edges of $G$, with two edges adjacent in $H$ when their four end vertices are distinct and form a clique in $G$. Then $H$ has 87 edges and 30 triangles. Each 6-clique of $G$ splits into three disjoint pairs in $\binom{6}{2}\binom{4}{2}/3! = 15$ ways, and each split is a triangle of $H$, so $30 = 15 \times 2$. A triangle detector on $H$ finds the 6-cliques of $G$, and a triangle counter counts them.

## Known algorithms

- *Brute force.* Try all $\binom{n}{k}$ sets and check each with the adjacency matrix: time $O(n^k k^2)$ on a RAM. This shows that p-Clique is in [XP](/xp/).
- *Nešetřil and Poljak (1985).* For $k = 3t$, build the graph $H$ whose vertices are the cliques of size $t$ of $G$, with an edge between two of them when their union is a clique of size $2t$. Then $G$ has a $k$-clique if and only if $H$ has a triangle. $H$ has at most $n^t$ vertices, and triangle detection by [matrix multiplication](/matrix-multiplication-exponent/) takes time $O(N^{\omega})$ on $N$ vertices. The total time is $O(n^{\omega k/3})$, where $\omega < 2.372$. For $n = 1000$ and $k = 6$, brute force looks at $\binom{1000}{6} = 1368173298991500$ sets, while $H$ has at most $\binom{1000}{2} = 499500$ vertices. For $k = 3$ this is triangle detection in time $O(n^{\omega})$; see the [triangle detection hypothesis](/triangle-detection-hypothesis/).
- *Other values of $k$.* When 3 does not divide $k$, Eisenbrand and Grandoni (2004) use rectangular matrix multiplication, which gives a slightly smaller exponent than fixing the remaining one or two vertices in all $n$ or $n^2$ ways.
- *Kernel.* p-Clique has no kernel of any size unless $\mathsf{FPT} = \mathsf{W}[1]$, because a decidable problem has a kernel if and only if it is FPT.

## Bounds

- *W[1]-completeness.* No algorithm in time $f(k) \cdot n^{O(1)}$ unless $\mathsf{FPT} = \mathsf{W}[1]$ (Downey and Fellows 1995). This says nothing about the exponent of the XP algorithm.
- *ETH bound.* Conditional on the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), there is no algorithm in time $f(k) \cdot n^{o(k)}$ for any computable $f$ (Chen, Huang, Kanj and Xia 2006; Theorem 14.21 in Cygan et al.). The idea is a reduction from a problem with $N$ variables to clique with $k$ classes of $2^{O(N/k)}$ vertices each, so that an $n^{o(k)}$ algorithm would give time $2^{o(N)}$. This is a separate result, and it is the reason the exponent must grow linearly in $k$.
- *Fine-grained bounds.* Whether $\omega k/3$ can be improved is open. Hypotheses about weighted cliques and hypercliques are stated on the [min-weight k-clique hypothesis](/min-weight-k-clique-hypothesis/) and [hyperclique hypothesis](/hyperclique-hypothesis/) pages.
- *Approximation.* Whether an FPT algorithm can find a clique of size $k/c$ when one of size $k$ exists is studied on [parameterized inapproximability](/parameterized-inapproximability/); the classical bounds for [maximum clique](/maximum-clique/) are on [clique inapproximability](/clique-inapproximability/).

## Reductions

- *To and from p-Independent-Set,* by the complement graph, with $k' = k$ and $O(n^2)$ time.
- *To multicolored clique,* with vertices $(i, v)$ for $1 \le i \le k$, with $k' = k$ and $O(k^2 n^2)$ time. See [parameterized reduction](/parameterized-reduction/).
- *To weighted 2-CNF satisfiability,* with one clause $\neg x_u \vee \neg x_v$ for each non-edge, $k' = k$. This puts the problem in W[1]. See [weighted satisfiability](/weighted-satisfiability/).
- *From every problem in W[1],* by the hardness proof of Downey and Fellows. See [clique is W[1]-complete](/clique-w1-completeness/).
- *From 3-coloring, for the ETH bound.* Split the $N$ vertices of a graph into $k$ groups of about $N/k$ vertices. Make one vertex for each proper 3-coloring of a group, and join two colorings of different groups when no edge between the two groups gets the same color at both ends; two colorings of the same group are never joined. A $k$-clique picks one coloring per group that fit together, so it is a proper 3-coloring of the whole graph, and back. The new graph has at most $k \cdot 3^{\lceil N/k \rceil}$ vertices. Under ETH, 3-coloring of graphs with $O(N)$ edges has no $2^{o(N)}$ algorithm, which gives the $n^{o(k)}$ bound.
- *To triangle detection,* by the Nešetřil and Poljak graph $H$, with $n^{k/3}$ vertices.

## Applications

- *Hardness proofs.* Most W[1]-hardness results in the literature reduce from clique or multicolored clique. Chapter 13 of Cygan et al. gives many such proofs.
- *Network analysis.* Cliques model dense groups in social and biological networks. The XP algorithm and the triangle method are practical for very small $k$, and the hardness explains why larger $k$ needs heuristics or structure such as small degeneracy.
- *Database queries.* A conjunctive query that joins one edge relation $\binom{k}{2}$ times asks for a $k$-clique. So the evaluation of conjunctive queries, with the query size as the parameter, is W[1]-hard as well.

## References
