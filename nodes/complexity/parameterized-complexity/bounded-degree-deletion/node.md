---
tag: CXX2BJ
kind: problem
slug: bounded-degree-deletion
name: Bounded degree deletion
aliases:
- d-degree deletion
- bounded-degree vertex deletion
area: complexity/parameterized-complexity
level: research
summary: "Delete at most k vertices so that every remaining vertex has degree at most d. For d = 0 this is vertex cover. FPT in k for fixed d, with time (d+2)^k n^O(1) and a kernel linear in k."
prereqs: [parameterized-vertex-cover, bounded-search-tree]
see_also: [parameterized-vertex-cover, nemhauser-trotter-theorem, kernelization, bounded-search-tree, w-hierarchy, odd-cycle-transversal, crown-reduction, lp-kernelization]
sources:
  - paper: doi:10.1016/j.jcss.2010.12.001
    title: "Michael R. Fellows, Jiong Guo, Hannes Moser and Rolf Niedermeier, A generalization of Nemhauser and Trotter's local optimization theorem, Journal of Computer and System Sciences 77(6), 1141-1158 (2011)"
    locator: the local optimization theorem for bounded degree deletion, the kernels with O(k) vertices for d at most 1 and O(k^(1+ε)) vertices for d at least 2, and W[2]-completeness when d is part of the input
  - paper: doi:10.1016/j.jcss.2016.08.003
    title: "Mingyu Xiao, On a generalization of Nemhauser and Trotter's local optimization theorem, Journal of Computer and System Sciences 84, 97-106 (2017)"
    locator: a kernel with a number of vertices linear in k for every fixed d
  - paper: doi:10.1016/0022-0000(80)90060-4
    title: "John M. Lewis and Mihalis Yannakakis, The node-deletion problem for hereditary properties is NP-complete, Journal of Computer and System Sciences 20(2), 219-230 (1980)"
    locator: NP-completeness of vertex deletion to any nontrivial hereditary property, which includes maximum degree at most d
---

Bounded degree deletion asks whether at most $k$ vertices can be deleted from a graph so that every remaining vertex has at most $d$ remaining neighbors. For $d = 0$ the rest has no edges, so the problem is [vertex cover](/parameterized-vertex-cover/). For $d = 1$ the rest is a matching plus isolated vertices, which is the same as having no path on three vertices. The problem is NP-hard for every fixed $d$, because graphs of maximum degree $d$ form a hereditary class (Lewis and Yannakakis, 1980). With the solution size $k$ as the [parameter](/parameter/) and $d$ fixed, it is [fixed-parameter tractable](/fixed-parameter-tractable/): a vertex of degree more than $d$ and $d + 1$ of its neighbors give a branching into $d + 2$ cases. Fellows, Guo, Moser and Niedermeier (2011) generalized the [Nemhauser and Trotter theorem](/nemhauser-trotter-theorem/) of vertex cover to this problem to get small kernels. When $d$ is part of the input, the problem with parameter $k$ is W[2]-complete. Graphs of bounded degree also arise from dense clusters: a vertex set induces an $s$-plex, a near-clique, exactly when it has degree at most $s - 1$ in the complement graph.

## In plain words

You have a network where some points have too many links. You may remove at most $k$ points, together with their links, and you want every point that is left to have at most $d$ links.

If $d$ is zero, nothing may stay linked at all, which is the vertex cover problem. Larger $d$ allows some links to stay.

Look at a point with too many links, together with $d + 1$ of its neighbors. One of these few points must go, so you can try each of them in turn. This gives a search whose cost grows with $k$ but only slowly with the size of the network. You can also shrink any input to an equivalent one whose size grows only linearly in $k$.

## Definition

**BOUNDED-DEGREE-DELETION**

- Instance: a graph $G = (V, E)$ and integers $d \ge 0$ and $k \ge 0$.
- Parameter: $k$, with $d$ a fixed constant. (With $d$ part of the input, the parameter can also be $k + d$.)
- Question: is there a set $X \subseteq V$ with $|X| \le k$ such that every vertex of $G - X$ has degree at most $d$ in $G - X$?

A certificate is the set $X$, checked in $O(n + m)$ time by counting the remaining neighbors of each remaining vertex. The smallest size of such a set is written $\mathrm{bdd}_d(G)$; so $\mathrm{bdd}_0(G)$ is the vertex cover number.

## Variants

- *$d = 0$.* [Vertex cover](/parameterized-vertex-cover/).
- *$d = 1$.* Delete vertices so that no path on three vertices is left as a subgraph. This is also called 3-path vertex cover, and its complement is a largest dissociation set.
- *$s$-plex deletion in the complement.* In the complement graph, a set $S$ is an $s$-plex if each of its vertices is adjacent to all but at most $s - 1$ others of $S$. So a largest $s$-plex of $G$ is the complement of a smallest solution of bounded degree deletion with $d = s - 1$ in the complement of $G$.
- *Edge version.* Delete at most $k$ edges so that the maximum degree is at most $d$. This form is solvable in polynomial time by matching methods, since it asks for a largest subgraph with degree bounds.
- *Other parameters.* With the parameter $k$ alone and $d$ in the input, the problem is W[2]-complete (Fellows, Guo, Moser and Niedermeier, 2011). See [the W hierarchy](/w-hierarchy/).

## Examples

Brute force over all vertex sets gives the values of $\mathrm{bdd}_d$ and the number of minimum solutions:

| graph | $d = 0$ | $d = 1$ | $d = 2$ | $d = 3$ |
|---|---|---|---|---|
| complete graph $K_5$ | 4 (5 solutions) | 3 (10) | 2 (10) | 1 (5) |
| $3 \times 3$ grid | 4 (1) | 4 (9) | 1 (1) | 1 (5) |
| Petersen graph | 6 (5) | 4 (5) | 3 (10) | 0 (1) |

The $3 \times 3$ grid shows that the value need not drop smoothly with $d$. For $d = 0$ and $d = 1$ it needs 4 deletions, but for $d = 2$ the center alone is enough: it is the only vertex of degree 4, and deleting it leaves an 8-cycle. For $d = 0$ the only minimum solution is the four middle vertices of the sides, the smaller side of the bipartition.

## Known algorithms

All bounds are on a word RAM, for fixed $d$; $n^{O(1)}$ factors are polynomial in $n$.

- *Branching.* Find a vertex $v$ of degree more than $d$ and $d + 1$ of its neighbors. Every solution contains one of these $d + 2$ vertices: if $v$ stays, at least one of the $d + 1$ neighbors must go. Branching on them gives a [bounded search tree](/bounded-search-tree/) with at most $(d + 2)^k$ leaves, so time $(d + 2)^k n^{O(1)}$. For $d = 0$ this is the $2^k$ algorithm of [vertex cover](/vertex-cover-branching/).
- *Local optimization theorem.* Fellows, Guo, Moser and Niedermeier (2011) generalize the [Nemhauser and Trotter theorem](/nemhauser-trotter-theorem/): in polynomial time, the vertex set splits into a part that some optimal solution contains, a part that can be removed, and a rest whose size is bounded in the solution size. This gives a kernel with $O(k)$ vertices for $d \le 1$ and with $O(k^{1+\varepsilon})$ vertices for every $\varepsilon > 0$ and $d \ge 2$.
- *Linear kernels for all d.* Xiao (2017) gives a kernel with a number of vertices linear in $k$ for every fixed $d$.

## Bounds

- *NP-hardness.* For every fixed $d \ge 0$, the problem is NP-complete (Lewis and Yannakakis, 1980), so no polynomial algorithm exists unless P = NP.
- *W[2]-hardness.* When $d$ is part of the input, the problem with parameter $k$ is W[2]-complete. So no algorithm in time $f(k) n^{O(1)}$ for all $d$ exists unless FPT = W[2], and the base of the exponent must depend on $d$.
- *Exponential time.* Already for $d = 0$, under the exponential time hypothesis there is no algorithm in time $2^{o(k)} n^{O(1)}$, as for vertex cover. That hypothesis is the weaker cousin of the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/).
- *Kernel size.* For $d = 0$ a kernel with $2k$ vertices exists, and kernels with $O(k)$ vertices exist for every fixed $d$.

## Reductions

- *From vertex cover.* The case $d = 0$ is vertex cover itself. For $d \ge 1$, add $d$ new pendant vertices to each vertex of $G$. A solution that deletes a pendant vertex stays a solution, of the same size or smaller, if it deletes the owner of that pendant instead. So assume that the solution $X$ has only old vertices. A vertex of $G$ that stays keeps its $d$ pendants, so it must lose all its old neighbors, and $X$ is a vertex cover of $G$. Conversely, every vertex cover of $G$ is a solution. So the minimum is the vertex cover number of $G$, with the same $k$.
- *W[2]-hardness.* With $d$ in the input, Fellows, Guo, Moser and Niedermeier give a parameterized reduction from a W[2]-hard problem in which $d$ grows with the input. For each fixed $d$ no such reduction can exist unless FPT = W[2], since the branching above is FPT.
- *To hitting set.* For fixed $d$, the problem is a $(d + 2)$-hitting set problem whose sets are the stars with $d + 1$ leaves. This gives the branching above and kernels by the [sunflower lemma](/sunflower-lemma/), though larger ones than the direct methods.

## Applications

- *Dense clusters.* In social and biological networks, $s$-plexes model groups that are nearly cliques. Searching for a large $s$-plex is bounded degree deletion in the complement graph, where the solution is often small.
- *Load limits.* In a network where each node may serve at most $d$ links, the problem asks for the fewest nodes to remove so that the rest respects the limit.
- *Structural parameter.* The distance to a graph of maximum degree $d$ is used as a parameter for other problems that are easy on graphs of bounded degree.

## References
