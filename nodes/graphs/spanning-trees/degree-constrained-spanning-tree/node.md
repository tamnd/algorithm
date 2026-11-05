---
tag: P2AD26
kind: problem
slug: degree-constrained-spanning-tree
name: Degree-constrained spanning tree problem
aliases:
- degree-bounded spanning tree
area: graphs/spanning-trees
level: advanced
summary: Find a spanning tree whose maximum vertex degree is bounded; NP-hard in general.
prereqs: [spanning-tree, minimum-spanning-tree, np-hard, hamiltonian-path-problem]
see_also: [hamiltonian-path-problem, maximum-leaf-spanning-tree, matroid-intersection, iterative-rounding, local-search, traveling-salesman-problem, lagrangian-relaxation, minimum-spanning-tree]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman (1979)
    locator: Appendix A2.1, problem ND1, Degree constrained spanning tree
  - paper: doi:10.1006/jagm.1994.1042
    title: "Martin Fürer and Balaji Raghavachari, Approximating the minimum-degree Steiner tree to within one of optimal, Journal of Algorithms 17(3) (1994), 409-423"
    locator: the whole paper (the local search that reaches the optimal maximum degree plus one)
  - paper: doi:10.1145/1250790.1250887
    title: "Mohit Singh and Lap Chi Lau, Approximating minimum bounded degree spanning trees to within one of optimal, Proceedings of the 39th ACM Symposium on Theory of Computing (2007), 661-670"
    locator: the whole paper (cost at most the optimum and each degree at most its bound plus one, by iterative rounding)
---

The degree-constrained spanning tree problem asks whether a connected undirected graph has a [spanning tree](/spanning-tree/) in which every vertex has degree at most $k$, and, in its optimization forms, for a spanning tree of least maximum degree or for a minimum weight spanning tree under degree bounds. For $k = 2$ a spanning tree of maximum degree 2 is a Hamiltonian path, so the problem is [NP-hard](/np-hard/) for each fixed $k \ge 2$. Two results make it one of the best understood NP-hard problems: Fürer and Raghavachari (1994) find in polynomial time a tree of maximum degree at most $\Delta^* + 1$, where $\Delta^*$ is the optimum, and Singh and Lau (2007) find a tree of weight at most the optimum that violates each degree bound by at most 1.

## In plain words

You must connect all the points of a network with a tree, but no point may have too many links, for example because each machine has only a few ports. Is there a tree in which every point has at most a given number of links?

If the limit is two links, the tree must be a single line through all points, and deciding whether such a line exists is a famous hard problem. So no fast exact method is known for any limit of two or more.

But a simple improvement method comes very close: it finds a tree whose busiest point has at most one link more than the best possible tree. A similar result holds when the links also have costs.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and an integer $k \ge 1$. For the weighted forms, also a weight $w(e)$ on each edge, real and possibly tied, and bounds $b_v \ge 1$ on the vertices.

**Decision form.** Does $G$ have a spanning tree $T$ with $\deg_T(v) \le k$ for each vertex $v$?

**Optimization forms.**

- **Minimum degree spanning tree.** Find a spanning tree that minimizes $\max_v \deg_T(v)$; call the optimum $\Delta^*(G)$.
- **Minimum bounded-degree spanning tree.** Find a spanning tree with $\deg_T(v) \le b_v$ for each $v$ and least total weight $w(T)$, or report that none exists.

**Disconnected graphs.** If $G$ is not connected, it has no spanning tree, and the question is asked for each component, with a spanning forest as the output.

**Edge cases.** For $k = 1$, a tree with all degrees at most 1 exists only for $n \le 2$. Self-loops are in no spanning tree. Parallel edges do not change the answer of the decision form; in the weighted form only the lightest copy matters.

## Variants

- **Degree bound at one vertex.** Find a minimum spanning tree in which one given vertex $r$ has degree at most $k$ (or exactly $k$). This is polynomial: the trees with $\deg_T(r) \le k$ are the common bases of the [graphic matroid](/graphic-matroid/) and a matroid that limits the edges at $r$, so weighted [matroid intersection](/matroid-intersection/) solves it, and Glover and Klingman, and Gabow and Tarjan, gave faster direct methods. It is used for the 1-tree bounds of the [traveling salesman problem](/traveling-salesman-problem/).
- **Minimum degree Steiner tree.** Connect only a given set of terminals; the Fürer-Raghavachari method extends to it with the same $+1$ guarantee.
- **Directed graphs.** Find a spanning arborescence with small out-degrees; it is harder to approximate, and only weaker guarantees are known.
- **[Maximum leaf spanning tree](/maximum-leaf-spanning-tree/).** A different degree objective: make as many vertices as possible have degree 1.

## Examples

**The star.** In $K_{1, n-1}$, the only spanning tree is the graph, so $\Delta^* = n - 1$. Any graph with a cut vertex whose removal leaves $c$ components has $\Delta^* \ge c$.

**A graph with six vertices.** Take the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. Of its 55 spanning trees, 17 have maximum degree 2 (Hamiltonian paths), 34 have maximum degree 3 and 4 have maximum degree 4, so $\Delta^* = 2$.

- The minimum spanning tree $\{bc, bd, ef, ac, ce\}$ of weight 13 has degree 3 at $c$, so it is the answer for $k = 3$ but not for $k = 2$.
- For $k = 2$, the lightest tree is the path $a, c, b, d, f, e$ with the edges $ac, bc, bd, df, ef$ and weight 14. Here the degree bound costs 1.

## Known algorithms

- **Exact.** Search over spanning trees, or dynamic programming over subsets in $O^*(2^n)$ time for the Hamiltonian case $k = 2$; integer programming in practice.
- **Fürer-Raghavachari local search, $\Delta^* + 1$.** Start from any spanning tree. Repeatedly look for a non-tree edge $uv$ whose ends have degree at most $\Delta - 2$, where $\Delta$ is the current maximum degree, and whose [fundamental cycle](/fundamental-cycle/) passes through a vertex of degree $\Delta$; swap the edge in and a tree edge at that vertex out. When no step applies, a witness set of vertices proves that $\Delta \le \Delta^* + 1$. The algorithm runs in $O(m n \alpha(m, n) \log n)$ time.
- **Singh-Lau iterative rounding, weighted.** Solve the linear program of the [spanning tree polytope](/spanning-tree-polytope/) with the degree bounds; take a basic optimal solution, remove the edges with value 0, and drop the degree bound of a vertex that has at most $b_v + 1$ fractional edges left; then solve again, until no degree bound is left and the solution is a tree. The result has weight at most the optimum of the linear program and degree at most $b_v + 1$ at each $v$. This is the main example of [iterative rounding](/iterative-rounding/).
- **Lagrangian relaxation.** Add a penalty $\lambda_v$ for each unit of degree above the bound to the edge weights, $w'(uv) = w(uv) + \lambda_u + \lambda_v$, solve the [minimum spanning tree](/minimum-spanning-tree/), and adjust $\lambda$; see [Lagrangian relaxation](/lagrangian-relaxation/). It gives lower bounds and good heuristics, without a guarantee.

## Bounds

- **NP-completeness.** The decision form is NP-complete for each fixed $k \ge 2$ (Garey and Johnson, ND1). For $k = 2$ it is the [Hamiltonian path problem](/hamiltonian-path-problem/). For $k > 2$, attach $k - 2$ new pendant vertices to each vertex of $G$: each old vertex then uses $k - 2$ of its $k$ allowed degrees on the new leaves, so the new graph has a spanning tree of maximum degree $k$ if and only if $G$ has a Hamiltonian path.
- **Additive approximation.** The $\Delta^* + 1$ bound is the best possible additive error for a polynomial algorithm unless P = NP, because the error 0 would decide Hamiltonian paths.
- **Weighted.** The Singh-Lau bound, weight at most the optimum and degree at most $b_v + 1$, is also the best of its kind unless P = NP, by the same argument. Earlier, Goemans (2006) had shown weight at most the optimum and degree at most $b_v + 2$.

## Reductions

- **From the Hamiltonian path problem,** as in the bounds above.
- **To matroid intersection** when only one vertex has a bound, as in the variants.
- **Relation to the traveling salesman problem.** A minimum weight spanning tree of maximum degree 2 is a shortest Hamiltonian path, so the weighted problem with $b_v = 2$ contains the path version of the traveling salesman problem.

## Applications

- **Network design.** Computer, telephone and sensor networks in which each node has a limited number of ports or radios, and multicast trees in which each router can copy a packet to only a few links.
- **Lower bounds for routing.** Degree-constrained trees at one vertex give the Held-Karp 1-tree bound for the traveling salesman problem.
- **Physical design.** Wiring problems where each pin can take only a few connections, and the layout of trees in VLSI circuits.

## References
