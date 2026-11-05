---
tag: AEC5V7
kind: problem
slug: minimum-weight-perfect-matching
name: Minimum-weight perfect matching
aliases:
- min-cost perfect matching
area: graphs/matching
level: advanced
summary: Find a perfect matching of smallest total weight; a subroutine of Christofides' algorithm.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the largest absolute value of an integer edge weight}
  time: {worst: O(n m + n^2 log n)}
prereqs: [perfect-matching, linear-programming-problem]
see_also: [maximum-weight-matching, matching-polytope, assignment-problem, hungarian-algorithm, christofides-algorithm, chinese-postman-problem, edmonds-blossom, jonker-volgenant-algorithm]
sources:
  - paper: doi:10.6028/jres.069B.013
    title: Jack Edmonds, Maximum matching and a polyhedron with 0,1-vertices, Journal of Research of the National Bureau of Standards 69B, 125 to 130 (1965)
    locator: the whole paper (the perfect matching polytope and the primal-dual algorithm)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 11, Weighted Matching (the weighted matching algorithm for perfect matchings, its proof and its running time)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 26, Weighted nonbipartite matching algorithmically, and Chapter 29, T-joins, undirected shortest paths, and the Chinese postman
  - paper: doi:10.1007/s12532-009-0002-8
    title: Vladimir Kolmogorov, Blossom V, a new implementation of a minimum cost perfect matching algorithm, Mathematical Programming Computation 1(1), 43 to 67 (2009)
    locator: the whole paper
  - paper: "William Cook and André Rohe, Computing minimum-weight perfect matchings, INFORMS Journal on Computing 11(2), 138 to 148 (1999)"
    locator: the whole paper (the Blossom IV implementation)
---

The minimum-weight perfect matching problem asks, for a graph with edge weights, for a [perfect matching](/perfect-matching/) of least total weight, or for the answer that the graph has no perfect matching. On a [bipartite graph](/bipartite-graph/) with equal sides it is the [assignment problem](/assignment-problem/). On a general graph, Edmonds solved it in 1965 by a primal-dual algorithm on the perfect matching polytope, and Gabow's implementation runs in $O(nm + n^2 \log n)$ time. It is the matching step of [Christofides' algorithm](/christofides-algorithm/) and of the [Chinese postman problem](/chinese-postman-problem/).

## In plain words

An even number of people must all be put into pairs, and each possible pair has a cost. Every person must be in exactly one pair. You want the pairs with the smallest total cost.

The difference from the problem of the best pairs with scores is the word "all". Nobody may be left alone, so sometimes a costly pair is needed to make the rest fit. If some people cannot be paired at all, for example because their number is odd, the answer is that no solution exists.

## Definition

Let $G = (V, E)$ be a finite undirected graph, general (odd cycles allowed) and weighted, with $n = |V|$, $m = |E|$ and a weight $w(e) \in \mathbb{R}$ for each edge. Weights may be negative. For integer weights, $N$ is the largest $|w(e)|$.

- **Input:** $G$ and $w$.
- **Output:** a perfect matching $M$ with the least $w(M) = \sum_{e \in M} w(e)$, or "infeasible" if $G$ has no perfect matching.

All perfect matchings have $n/2$ edges, so adding a constant $c$ to every weight adds $cn/2$ to every solution. Because of this, the sign of the weights does not matter, and minimizing $w$ is the same as maximizing $-w$.

**Linear programming form.** By Edmonds' theorem, the optimum, when it exists, equals
$$\min\; w^{\mathsf T} x \quad \text{subject to} \quad x \ge 0, \;\; x(\delta(v)) = 1 \;(v \in V), \;\; x(\delta(U)) \ge 1 \;(U \subseteq V, |U| \text{ odd}, |U| \ge 3),$$
the [matching polytope](/matching-polytope/) of perfect matchings. The dual is
$$\max\; \sum_{v} y_v + \sum_{U} z_U \quad \text{subject to} \quad z_U \ge 0, \;\; y_u + y_v + \sum_{U :\, uv \in \delta(U)} z_U \le w(uv) \;(uv \in E),$$
with $y$ free. A perfect matching $M$ and a dual solution are both optimal if and only if each edge of $M$ is tight, meaning that its dual constraint holds with equality, and each odd set with $z_U > 0$ has exactly one edge of $M$ in $\delta(U)$.

## Variants

- **Bipartite graphs.** Only the degree equalities are needed: the [assignment problem](/assignment-problem/). The [Hungarian algorithm](/hungarian-algorithm/), the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/) and the [auction algorithm](/auction-algorithm/) solve it.
- **Complete graphs with metric weights.** In [Christofides' algorithm](/christofides-algorithm/) the graph is complete on an even set of points and the weights satisfy the triangle inequality. For points in the plane with Euclidean distances, faster exact algorithms and approximation schemes exist that use geometry.
- **Maximum-weight matching.** No perfect matching is required: [maximum-weight matching](/maximum-weight-matching/). The two problems reduce to each other.
- **Bottleneck version.** Minimize the largest weight of an edge in the perfect matching instead of the sum: [bottleneck matching](/bottleneck-matching/), solved by binary search over a threshold and a cardinality test.
- **T-joins.** Given an even set $T$ of vertices, find a least-weight set of edges whose odd-degree vertices are exactly $T$. With nonnegative weights this reduces to minimum-weight perfect matching on $T$ with shortest-path distances.

## Examples

**Three perfect matchings of $K_4$.** Let $V = \{a, b, c, d\}$ with $w(ab) = w(cd) = 1$, $w(ac) = w(bd) = 2$ and $w(ad) = w(bc) = 3$. The perfect matchings are $\{ab, cd\}$ with weight 2, $\{ac, bd\}$ with weight 4, and $\{ad, bc\}$ with weight 6. The optimum is $\{ab, cd\}$. A dual solution that proves it is $y_a = y_b = y_c = y_d = \frac12$ and $z = 0$: every edge has $y_u + y_v = 1 \le w(uv)$, the edges $ab$ and $cd$ are tight, and $\sum_v y_v = 2$.

**An odd cycle that forces a costly edge.** Take the 5-cycle $v_1 v_2 v_3 v_4 v_5$ with weight 1 on each edge, and a vertex $t$ with $w(t v_1) = 10$. The graph has 6 vertices, and $t$ has only one edge, so every perfect matching contains $t v_1$. Then $v_2 v_3 v_4 v_5$ is a path with the single perfect matching $\{v_2 v_3, v_4 v_5\}$. The optimum $\{t v_1, v_2 v_3, v_4 v_5\}$ has weight 12, though its heaviest edge alone is 10.

**Negative weights.** On the 4-cycle $a b c d$ with $w(ab) = w(cd) = -5$ and $w(bc) = w(da) = 1$, the optimum is $\{ab, cd\}$, of weight $-10$. Adding 5 to every weight gives the weights $0, 6, 0, 6$ and the same optimum, of weight 0, as every solution moves by $5 \cdot 2 = 10$.

**No perfect matching.** The triangle with any weights, the star $K_{1,3}$, and any graph with an odd number of vertices are infeasible. The graph made of a center joined to three triangles has 10 vertices and is also infeasible, by [Tutte's theorem](/tutte-theorem/).

**The empty graph.** With no vertices, the empty matching is perfect, of weight 0.

## Known algorithms

| algorithm | graphs | time |
|---|---|---|
| [Hungarian algorithm](/hungarian-algorithm/) | bipartite | $O(n^3)$, or $O(nm + n^2 \log n)$ with Fibonacci heaps |
| [Jonker-Volgenant](/jonker-volgenant-algorithm/) | bipartite | $O(n^3)$, fast in practice |
| Edmonds' primal-dual blossom algorithm | general | $O(n^3)$ in the implementations of Gabow and Lawler |
| Gabow's implementation | general | $O(nm + n^2 \log n)$ |
| Duan-Pettie-Su scaling | general, integer weights | $O(m \sqrt n \log(nN))$ |
| Blossom IV (Cook and Rohe), Blossom V (Kolmogorov) | general | the same worst case; fast in practice |

Edmonds' algorithm keeps a feasible dual $(y, z)$ and a matching of tight edges. It grows alternating trees from exposed vertices along tight edges. When a tree edge joins two even vertices of the same tree, it shrinks the odd cycle into a blossom $U$, which may get $z_U > 0$. When it joins two trees, it augments. When neither is possible, it changes the duals: $y$ grows on even vertices and shrinks on odd ones, $z_U$ grows on even blossoms and shrinks on odd ones, until an edge becomes tight or an odd blossom reaches $z_U = 0$ and is expanded. Each step keeps the dual feasible and the matching edges tight, so at the end, when the matching is perfect, complementary slackness proves it optimal. If an alternating forest cannot grow and the duals can increase without bound, the graph has no perfect matching.

## Bounds

- **Upper bounds.** $O(nm + n^2 \log n)$ strongly polynomial, and $O(m \sqrt n \log(nN))$ for integer weights, on the [word RAM](/word-ram/).
- **Lower bound.** $\Omega(n + m)$, the size of the input.
- **Feasibility.** Deciding whether any perfect matching exists already costs as much as [maximum matching](/maximum-matching/), $O(m \sqrt n)$ with the known algorithms.

## Reductions

- **To and from maximum-weight matching.** For the direction from this problem, replace $w(e)$ by $C - w(e)$ with $C > \sum_e |w(e)|$: a maximum-weight matching then has as many edges as possible, so it is perfect when a perfect matching exists, and among those it has the least $w$. For the other direction, take two copies of the graph and join each vertex to its copy by an edge of weight 0; see [maximum-weight matching](/maximum-weight-matching/).
- **T-joins and the Chinese postman problem.** Let $T$ be the set of odd-degree vertices of a connected graph with nonnegative weights. Compute [all-pairs shortest paths](/all-pairs-shortest-paths/) between the vertices of $T$, and find a minimum-weight perfect matching of the complete graph on $T$ with these distances. The union of the matched paths is a minimum T-join. Adding it to the graph makes all degrees even, and an [Eulerian circuit](/eulerian-circuit/) of the result is an optimal postman tour.
- **Christofides' algorithm.** Find a [minimum spanning tree](/minimum-spanning-tree/), and add a minimum-weight perfect matching on its odd-degree vertices. The result has an Eulerian circuit, and shortcutting it gives a tour of at most $\frac32$ times the optimum for the [metric TSP](/metric-tsp/).
- **Bipartite case to min-cost flow.** With unit capacities from a source to $L$, from $L$ to $R$ with cost $w$, and from $R$ to a sink, a [min-cost flow](/min-cost-flow-problem/) of value $|L| = |R|$ is an optimal perfect matching.

## Applications

- **Routing.** Christofides' algorithm for the traveling salesman problem, the Chinese postman problem for street sweeping and mail delivery, and the planning of pen moves in plotters.
- **Quantum error correction.** Decoders for surface codes match the detected errors in pairs by a minimum-weight perfect matching, where the weight of a pair is the length of the most likely error chain between them.
- **Physics.** Finding a ground state of an Ising spin glass on a planar lattice reduces to a minimum-weight perfect matching.
- **Assignment.** In the bipartite case, assigning workers to jobs or tracking objects between two video frames at least total cost.

## References
