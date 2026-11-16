---
tag: N5T7DJ
kind: problem
slug: parameterized-independent-set
name: Parameterized independent set
aliases: []
area: complexity/parameterized-complexity
level: core
summary: "Decide whether a graph has an independent set of size k, with k as the parameter. W[1]-complete in general, but FPT on planar graphs and on graphs of bounded degree."
prereqs: [independent-set, fixed-parameter-tractable]
see_also: [parameterized-clique, clique-w1-completeness, parameterized-vertex-cover, maximum-independent-set, independent-set, weighted-satisfiability, para-np-hardness, planar-graph]
sources:
  - paper: doi:10.1016/0304-3975(94)00097-3
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness II: on completeness for W[1], Theoretical Computer Science 141(1-2), 109-131 (1995)"
    locator: the main theorem, independent set is W[1]-complete
  - paper: doi:10.1016/j.jcss.2006.04.007
    title: "Jianer Chen, Xiuzhen Huang, Iyad A. Kanj and Ge Xia, Strong computational lower bounds via parameterized complexity, Journal of Computer and System Sciences 72(8), 1346-1367 (2006)"
    locator: no f(k) n^o(k) algorithm for independent set unless ETH fails
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13 (W[1]-hardness of independent set) and Theorem 14.21 (the ETH lower bound for clique and independent set)
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: "Michael R. Garey, David S. Johnson and Larry J. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237-267 (1976)"
    locator: vertex cover, and so independent set, stays NP-complete on planar graphs of maximum degree 3
---

Parameterized independent set, p-Independent-Set, asks whether a graph has $k$ vertices with no edge between any two of them, with the size $k$ as the [parameter](/parameter/). It is W[1]-complete (Downey and Fellows 1995), so it has no algorithm in time $f(k) \cdot n^{O(1)}$ unless $\mathsf{FPT} = \mathsf{W}[1]$, and none in time $f(k) \cdot n^{o(k)}$ unless the Exponential Time Hypothesis fails. On [planar graphs](/planar-graph/) and on graphs of bounded degree it becomes FPT, because large graphs of these kinds always have large independent sets. This page gives the parameterized view only; the [independent set](/independent-set/) page has the classical problem, and [maximum independent set](/maximum-independent-set/) has the exact exponential algorithms.

## In plain words

You want to pick a given number of points in a network so that no two picked points are joined by a line. Think of guests at a dinner where some pairs must not sit at the same table.

In general nobody knows a method that is fast when the number of picked points is small; it is the same problem as finding a group of mutual friends, with the friendships turned around. But if every point has few lines, or the network can be drawn flat without crossings, a large network always has many points with no lines between them. Then either the network is large and the answer is yes at once, or it is small and you can check it fully.

## Definition

The input is a graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, given by adjacency lists, and a number $k$. A set $S \subseteq V$ is *independent* if no edge has both ends in $S$. The largest size of an independent set is $\alpha(G)$.

**p-INDEPENDENT-SET**

- Instance: a graph $G = (V, E)$ and an integer $k \ge 0$.
- Parameter: $k$.
- Question: does $G$ have an independent set $S$ with $|S| = k$?

A subset of an independent set is independent, so the question is the same as $\alpha(G) \ge k$. A yes-instance has a certificate of $k$ vertex names.

**Complexity.** p-Independent-Set is W[1]-complete under [parameterized reductions](/parameterized-reduction/); this is the main theorem of Downey and Fellows (1995, Theoretical Computer Science 141). The proof is outlined on [clique is W[1]-complete](/clique-w1-completeness/). The classical problem, with $k$ part of the input, is NP-complete.

## Variants

- *Parameter $n - k$.* $S$ is independent exactly when $V \setminus S$ is a vertex cover. With the parameter $n - k$ the problem is [p-Vertex-Cover](/parameterized-vertex-cover/), which is FPT with a kernel of $2k$ vertices. The two parameterizations of the same classical problem are on opposite sides of the FPT line.
- *Bounded degree.* If every vertex has degree at most $\Delta$, a greedy pass (take a vertex, delete it and its neighbors, repeat) gives an independent set of at least $\lceil n/(\Delta + 1) \rceil$ vertices. So if $n \ge (\Delta + 1) k$ the answer is yes, and otherwise the graph has fewer than $(\Delta + 1) k$ vertices, a kernel. With the parameter $k + \Delta$ the problem is FPT. With the parameter $\Delta$ alone it is not: independent set is NP-complete on planar graphs of maximum degree 3 (Garey, Johnson and Stockmeyer 1976), so it is [para-NP-hard](/para-np-hardness/) in $\Delta$.
- *Planar graphs.* By the [four color theorem](/four-color-theorem/), a planar graph has an independent set of at least $\lceil n/4 \rceil$ vertices, the largest color class. So if $n \ge 4k$ the answer is yes, and otherwise $n < 4k$, a kernel of fewer than $4k$ vertices. A planar graph on $n$ vertices has [treewidth](/treewidth/) $O(\sqrt{n})$, so [dynamic programming on a tree decomposition](/dp-on-tree-decompositions/) of the kernel takes time $2^{O(\sqrt{k})} n^{O(1)}$.
- *Treewidth.* With the treewidth $t$ of a given tree decomposition as the parameter, dynamic programming decides the problem in time $2^t t^{O(1)} n$, for any $k$.
- *Multicolored independent set.* One vertex from each of $k$ given classes. It is W[1]-complete, by the multicolored clique map on the complement.
- *Counting.* Counting the independent sets of size $k$ is #W[1]-complete; see [parameterized counting complexity](/parameterized-counting-complexity/).

## Examples

The Petersen graph has 10 vertices, 15 edges and degree 3 at every vertex. Its numbers of independent sets of sizes 1 to 5 are 10, 30, 30, 5 and 0. So $\alpha = 4$: (Petersen, 4) is a yes-instance and (Petersen, 5) is a no-instance. The bounded-degree rule gives $\lceil 10/4 \rceil = 3$ at once, so the rule answers yes for every $k \le 3$ without a search.

The complement of the Petersen graph has $45 - 15 = 30$ edges. Its cliques are the independent sets of the Petersen graph, so it has 5 cliques of size 4 and none of size 5.

The house graph (a square 0, 1, 2, 3 and a roof vertex 4 joined to 0 and 1) has $\alpha = 2$: the sets $\{0, 2\}$, $\{1, 3\}$, $\{2, 4\}$ and $\{3, 4\}$ are its four independent sets of size 2. Its least vertex cover has $5 - 2 = 3$ vertices.

## Known algorithms

- *Brute force.* Try all $\binom{n}{k}$ sets: time $O(n^k k^2)$ with an adjacency matrix. The problem is in [XP](/xp/).
- *Matrix multiplication.* Apply the Nešetřil and Poljak algorithm for [clique](/parameterized-clique/) to the complement graph: time $O(n^{\omega k/3})$ when 3 divides $k$, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/).
- *Restricted classes.* Kernels of fewer than $(\Delta + 1) k$ vertices on graphs of maximum degree $\Delta$ and fewer than $4k$ vertices on planar graphs, as above.
- *Exact algorithms in $n$.* The best algorithms for [maximum independent set](/maximum-independent-set/) run in time $O(c^n)$ for constants $c < 2$. They do not use $k$.

## Bounds

- *W[1]-completeness.* No algorithm in time $f(k) \cdot n^{O(1)}$ unless $\mathsf{FPT} = \mathsf{W}[1]$. There is also no kernel of any size unless $\mathsf{FPT} = \mathsf{W}[1]$, because a decidable problem has a kernel if and only if it is FPT.
- *ETH bound.* Conditional on the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), there is no algorithm in time $f(k) \cdot n^{o(k)}$ for any computable $f$ (Chen, Huang, Kanj and Xia 2006; Theorem 14.21 in Cygan et al.). This bound is separate from the W[1]-hardness.
- *Classical.* The problem is NP-complete, so no algorithm runs in time polynomial in $n$ and $k$ unless P = NP.

## Reductions

- *To and from p-Clique,* by the [complement graph](/complement-graph/): $(G, k) \mapsto (\overline{G}, k)$, $k' = k$, $O(n^2)$ time.
- *To and from weighted antimonotone 2-CNF satisfiability:* one clause $\neg x_u \vee \neg x_v$ for each edge $uv$, with $k' = k$. See [weighted satisfiability](/weighted-satisfiability/).
- *To vertex cover, but not as a parameterized reduction.* $(G, k) \mapsto (G, n - k)$ is a polynomial-time reduction, and its new parameter $n - k$ depends on $n$. So the W[1]-hardness of independent set does not move to vertex cover.
- *To d-set packing.* Give each vertex $v$ the set of edges at $v$. Two such sets are disjoint exactly when the two vertices are not adjacent, so an independent set of size $k$ is a packing of $k$ sets, with $k' = k$. On a graph of maximum degree $\Delta$ the sets have at most $\Delta$ elements, and [d-set packing](/parameterized-set-packing/) is FPT for each fixed $d$.

## Applications

- *Conflict-free selection.* Choosing $k$ tasks, frequencies or sites with no conflicting pair is independent set in the conflict graph. The hardness explains why large general instances need heuristics, and the planar and bounded-degree kernels explain why many geometric instances are easy for small $k$.
- *Source of hardness.* Independent set is the problem that Downey and Fellows proved W[1]-complete. Many reductions start from its multicolored form.

## References
