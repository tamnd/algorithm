---
tag: TQS7C3
kind: definition
slug: edge-cover
name: Edge cover
area: graphs/matching
level: intro
summary: A set of edges that touches every vertex of the graph.
prereqs: [graph]
see_also: [minimum-edge-cover, gallai-identity, maximum-matching, perfect-matching, vertex-cover, independent-set, bipartite-matching]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (edge covers, the edge cover number and Gallai's identity)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 19.1, Matchings, edge covers, and Gallai's theorem, and Chapter 27, Nonbipartite edge cover
---

An edge cover of a [graph](/graph/) is a set of edges such that each vertex is an end of at least one edge of the set. The least size of an edge cover is the edge cover number $\rho(G)$. It is the covering partner of the matching number: by [Gallai's identity](/gallai-identity/), a graph with $n$ vertices and no isolated vertex has $\rho(G) = n - \nu(G)$, where $\nu(G)$ is the size of a [maximum matching](/maximum-matching/). The definition is the same for bipartite and general graphs, and for weighted and unweighted graphs.

## Definition

Let $G = (V, E)$ be a finite undirected graph. Parallel edges are allowed. A set $F \subseteq E$ is an **edge cover** of $G$ if

$$\forall v \in V \;\; \exists e \in F : \; v \in e.$$

We say that $F$ *covers* $v$ when some edge of $F$ has $v$ as an end.

- $G$ has an edge cover if and only if $G$ has no isolated vertex. If $v$ is isolated, no edge has $v$ as an end. If no vertex is isolated, $E$ itself is an edge cover.
- The **edge cover number** $\rho(G)$ is the least size of an edge cover. Some books write $\beta'(G)$. It is defined only when $G$ has no isolated vertex. The graph with no vertices has the edge cover $\emptyset$, so $\rho = 0$.
- A **minimum edge cover** is an edge cover of size $\rho(G)$. A **minimal edge cover** is an edge cover $F$ such that no proper subset of $F$ is an edge cover. Each minimum edge cover is minimal. The converse is false (see the examples).
- When each edge $e$ has a weight $w(e)$, a **minimum-weight edge cover** is an edge cover $F$ with the least total weight $\sum_{e \in F} w(e)$. The problem of finding one is the [minimum edge cover](/minimum-edge-cover/) problem.

**Lower bound.** Each edge covers at most two vertices, so $\rho(G) \ge \lceil n/2 \rceil$ for $n = |V|$. Equality with $n$ even holds if and only if $G$ has a [perfect matching](/perfect-matching/): an edge cover with $n/2$ edges covers $n$ vertices, so its edges have no common end.

**Structure.** Each minimal edge cover $F$ is a forest of stars. *Proof.* Let $e = uv \in F$. If both $u$ and $v$ were covered by other edges of $F$, then $F \setminus \{e\}$ would be an edge cover, against minimality. So each edge of $F$ has an end of degree 1 in the subgraph $(V, F)$. A cycle in $(V, F)$ has only vertices of degree at least 2, so there is none. A path with three edges in $(V, F)$ has a middle edge with both ends of degree at least 2, so there is none. A tree with no path of three edges has diameter at most 2, so it is a star. $\square$

## Examples and non-examples

The numbers below are for small named graphs with $n$ vertices.

| graph | $n$ | $\rho(G)$ | a minimum edge cover |
|---|---|---|---|
| path $P_5$: $v_1 v_2 v_3 v_4 v_5$ | 5 | 3 | $\{v_1v_2, v_3v_4, v_4v_5\}$ |
| path $P_6$ | 6 | 3 | $\{v_1v_2, v_3v_4, v_5v_6\}$ |
| cycle $C_5$ | 5 | 3 | two disjoint edges and one edge at the fifth vertex |
| complete graph $K_5$ | 5 | 3 | $\{12, 34, 45\}$ |
| complete bipartite $K_{2,3}$ | 5 | 3 | one edge at each vertex of the side of size 3 |
| star $K_{1,4}$ | 5 | 4 | all four edges |
| Petersen graph | 10 | 5 | a perfect matching |

In general, $\rho(P_n) = \rho(C_n) = \rho(K_n) = \lceil n/2 \rceil$ for $n \ge 2$ (for $C_n$, $n \ge 3$), and $\rho(K_{a,b}) = \max(a, b)$ for $a, b \ge 1$. Each of these values is $n - \nu(G)$, as Gallai's identity says.

- **Minimal but not minimum.** In $P_6$ with vertices $v_1, \ldots, v_6$, the set $\{v_1v_2, v_2v_3, v_4v_5, v_5v_6\}$ is an edge cover. It is minimal: each edge has an end of degree 1 in the set ($v_1$, $v_3$, $v_4$, $v_6$), so no edge can go. Its size is 4, but $\rho(P_6) = 3$.
- **Non-example: an isolated vertex.** The graph with vertices $\{a, b, c\}$ and the one edge $ab$ has no edge cover, because nothing covers $c$.
- **Non-example: a maximum matching that is not perfect.** In $C_5$, two disjoint edges form a maximum matching, but they leave one vertex uncovered. So a maximum matching is an edge cover only when it is perfect.
- **Non-example: a vertex cover.** In $P_3 = abc$, the set $\{b\}$ is a vertex cover: vertices that touch every edge. An edge cover goes the other way: edges that touch every vertex. Here $\{ab, bc\}$ is the only edge cover.
- **Weighted.** In the triangle $abc$ with $w(ab) = 1$, $w(bc) = 1$, $w(ca) = 5$, the minimum-weight edge cover is $\{ab, bc\}$ with weight 2. Each edge cover has at least two edges, and the other two pairs weigh 6.

## Related definitions

- **Matching.** A set of edges with no common end. Matchings are the packing partner of edge covers. A minimum edge cover comes from a maximum matching by adding one edge at each uncovered vertex, and a maximum matching comes from a minimum edge cover by keeping one edge of each star. These two maps prove [Gallai's identity](/gallai-identity/). See [maximum matching](/maximum-matching/).
- **Perfect matching.** A matching that is also an edge cover. See [perfect matching](/perfect-matching/).
- **Vertex cover and independent set.** A [vertex cover](/vertex-cover/) is a set of vertices that meets every edge, and an [independent set](/independent-set/) is its complement. Gallai's other identity says $\alpha(G) + \tau(G) = n$ for these two numbers. In a [bipartite graph](/bipartite-graph/), Kőnig's theorems give $\nu = \tau$ and $\alpha = \rho$ (the second when there is no isolated vertex).
- **Minimum edge cover problem.** Find an edge cover of least size or weight. It is solvable in polynomial time through matching, unlike the [NP-complete](/np-complete/) vertex cover problem. See [minimum edge cover](/minimum-edge-cover/).
- **b-edge cover.** Each vertex $v$ must be covered at least $b(v)$ times. It is the covering form of [b-matching](/b-matching/).

## References
