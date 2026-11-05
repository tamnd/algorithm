---
tag: M822MC
kind: definition
slug: complete-graph
name: Complete graph
aliases:
- K_n
area: graphs/graph-representation
level: intro
summary: Simple graph in which every pair of distinct vertices is joined by an edge.
prereqs: [graph, degree]
see_also: [complement-graph, clique, dense-graph, regular-graph, bipartite-graph, ramsey-theorem, turan-theorem, counting-spanning-trees]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1 (Graphs), the complete graph K^n; Section 4.2 (Plane graphs) for the non-planarity of K^5; Chapter 7 (Extremal graph theory) for Turan's theorem
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1 (complete graphs and cliques), and Section 2.2 (Cayley's formula for the spanning trees of K_n)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the complete graph; Section 34.5.1 (The clique problem)
---

The complete graph $K_n$ is the simple undirected [graph](/graph/) on $n$ vertices in which each two distinct vertices are joined by an [edge](/edge/). It has $\binom{n}{2} = n(n-1)/2$ edges, the most a simple graph on $n$ vertices can have, and each vertex has [degree](/degree/) $n - 1$. A set of vertices that induces a complete graph in a larger graph is a [clique](/clique/). $K_n$ is the extreme case of a [dense graph](/dense-graph/), and its [complement](/complement-graph/) is the graph with no edges.

## Definition

For a finite set $V$ with $|V| = n$, the **complete graph** on $V$ is

$$K_V = \left(V, \binom{V}{2}\right), \qquad \binom{V}{2} = \{\{u, v\} : u, v \in V,\ u \ne v\}.$$

Up to isomorphism it depends only on $n$, and it is written $K_n$. Its basic counts are:

- $m = |E(K_n)| = \binom{n}{2}$;
- $d(v) = n - 1$ for each vertex $v$, so $K_n$ is $(n-1)$-[regular](/regular-graph/);
- its diameter is 1 for $n \ge 2$: each two distinct vertices are at distance 1.

**Directed version.** The *complete directed graph* on $V$ has all $n(n-1)$ ordered pairs $(u, v)$ with $u \ne v$ as edges. With self-loops, as CLRS allows, the full relation $V \times V$ has $n^2$ edges. A *tournament* is an orientation of $K_n$: exactly one of $(u, v)$ and $(v, u)$ for each pair.

**Complete bipartite graph.** $K_{p, q}$ has a vertex set split into parts $A$ and $B$ with $|A| = p$ and $|B| = q$, and all $pq$ edges between $A$ and $B$, and none inside a part. It is a [bipartite graph](/bipartite-graph/), and it is not a complete graph for $p + q \ge 3$.

**Clique.** A set $S \subseteq V$ in a graph $G$ is a [clique](/clique/) when each two distinct vertices of $S$ are adjacent, that is, when the [induced subgraph](/induced-subgraph/) $G[S]$ is complete. The [clique number](/clique-number/) $\omega(G)$ is the size of a largest clique.

## Examples and non-examples

**Small cases.** $K_1$ is a single vertex. $K_2$ is a single edge. $K_3$ is the triangle. $K_4$ is the graph of the tetrahedron.

| $n$ | edges $\binom{n}{2}$ | degree | spanning trees $n^{n-2}$ | planar |
|---|---|---|---|---|
| 1 | 0 | 0 | 1 | yes |
| 2 | 1 | 1 | 1 | yes |
| 3 | 3 | 2 | 3 | yes |
| 4 | 6 | 3 | 16 | yes |
| 5 | 10 | 4 | 125 | no |
| 6 | 15 | 5 | 1296 | no |
| 10 | 45 | 9 | 100000000 | no |

The count of spanning trees is Cayley's formula $n^{n-2}$, which also follows from the [matrix-tree theorem](/matrix-tree-theorem/); see [counting spanning trees](/counting-spanning-trees/). $K_5$ is not [planar](/planar-graph/): a simple planar graph with $n \ge 3$ vertices has at most $3n - 6$ edges, and $K_5$ has $10 > 3 \cdot 5 - 6 = 9$. So $K_n$ is planar exactly for $n \le 4$.

**Representation.** $K_n$ is the worst case for an [adjacency list](/adjacency-list/), which holds $2\binom{n}{2} = n(n-1)$ entries, and for each algorithm whose cost depends on $m$. An [adjacency matrix](/adjacency-matrix/) of $K_n$ has 1 in each cell off the diagonal. A program can also store $K_n$ as an [implicit graph](/implicit-graph/): the rule "$u$ and $v$ are adjacent when $u \ne v$" needs $O(1)$ space, answers an adjacency query in $O(1)$ time and lists the $n - 1$ neighbours of a vertex in $\Theta(n)$ time.

**Where complete graphs appear.**

- The [metric travelling salesman problem](/metric-tsp/) takes a complete graph with a distance on each edge.
- [Ramsey's theorem](/ramsey-theorem/): each 2-coloring of the edges of $K_6$ has a triangle in one color, and $K_5$ has a coloring without one, so $R(3, 3) = 6$.
- [Turán's theorem](/turan-theorem/): the most edges in a graph on $n$ vertices without a $K_{r+1}$.
- The [clique problem](/clique-problem/): decide whether a graph contains $K_k$. It is NP-complete when $k$ is part of the input.

**Non-examples.**

- The cycle on 4 vertices is not complete: it misses the two diagonals, so it has 4 edges, not $\binom{4}{2} = 6$.
- $K_{2, 2}$ is the same 4-cycle, and $K_{1, 3}$ is a star; neither is complete.
- A [multigraph](/multigraph/) with two parallel edges between each pair is not $K_n$, because $K_n$ is simple.
- In a complete directed graph, both $(u, v)$ and $(v, u)$ are edges, so a tournament is not a complete directed graph for $n \ge 2$.

## Related definitions

- [Clique](/clique/) and [clique number](/clique-number/): complete subgraphs inside a graph.
- [Complement graph](/complement-graph/): the complement of $K_n$ is the empty graph $\overline{K_n}$, with $n$ vertices and no edges.
- [Regular graph](/regular-graph/): $K_n$ is $(n-1)$-regular.
- [Dense graph](/dense-graph/): graphs with $\Theta(n^2)$ edges, of which $K_n$ is the densest.
- [Bipartite graph](/bipartite-graph/) and the complete bipartite graph $K_{p,q}$.

## References
