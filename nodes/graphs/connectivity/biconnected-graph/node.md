---
tag: WHGC75
kind: definition
slug: biconnected-graph
name: Biconnected graph
aliases:
- 2-connected graph
- Nonseparable graph
area: graphs/connectivity
level: core
summary: A connected graph with at least three vertices and no articulation point.
prereqs: [connected-graph, articulation-point]
see_also: [biconnected-components, hopcroft-tarjan-biconnectivity, ear-decomposition, k-vertex-connected-graph, two-edge-connected-graph, menger-theorem, block-cut-tree, st-numbering]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 3.1, 2-connected graphs and subgraphs (the construction of every 2-connected graph from a cycle by adding paths)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.2, k-connected graphs (Whitney's characterization of 2-connected graphs and its equivalent forms)
  - paper: doi:10.1090/S0002-9947-1932-1501641-2
    title: Hassler Whitney, Non-separable and planar graphs, Transactions of the American Mathematical Society 34(2), 339 to 362 (1932)
    locator: the characterization of non-separable graphs by cycles through two vertices
---

A biconnected graph is a [connected graph](/connected-graph/) with at least three vertices that has no [articulation point](/articulation-point/): removing any one vertex leaves it connected. By Whitney's theorem this is the same as saying that every two vertices lie on a common cycle, or that every two vertices are joined by two paths that share no inner vertex. Biconnected graphs are the [2-vertex-connected graphs](/k-vertex-connected-graph/), the pieces into which the [biconnected components](/biconnected-components/) split a graph, and the input class of many algorithms on planar graphs, such as [st-numbering](/st-numbering/).

## Definition

Let $G = (V, E)$ be an [undirected graph](/undirected-graph/) with $n = |V|$. Parallel edges and [self-loops](/self-loop/) are allowed, but they play no part: the definition depends only on which pairs of distinct vertices are adjacent.

$G$ is **biconnected** (or **2-connected**) if $n \ge 3$, $G$ is connected, and $G - v$ is connected for every vertex $v$.

**Theorem (Whitney, 1932).** For a graph $G$ with $n \ge 3$, these are equivalent:

1. $G$ is biconnected.
2. Every two distinct vertices lie on a common cycle.
3. Every two distinct vertices $u, v$ are joined by two paths that have only $u$ and $v$ in common.

*Proof.* (2) and (3) say the same thing, since a cycle through $u$ and $v$ is the union of two such paths, and two such paths form a cycle.

(3) implies (1). $G$ is connected by (3). Suppose $G - x$ is not connected, and take $u$ and $w$ in two different components of $G - x$. By (3) there are two $u$-$w$ paths with only $u$ and $w$ in common. At most one of them passes through $x$, so the other one joins $u$ and $w$ in $G - x$, a contradiction.

(1) implies (3), by induction on the distance $d(u, v)$. If $d(u, v) = 1$, let $e$ be an edge $uv$. The graph $G - e$ is connected: otherwise one of its two parts has at least two vertices, since $n \ge 3$, and then $u$ or $v$ would be an articulation point of $G$. So $G - e$ has a $u$-$v$ path, and this path and the edge $e$ are the two paths. The path may be a parallel copy of $e$. If $d(u, v) = k \ge 2$, let $w$ be the vertex before $v$ on a shortest $u$-$v$ path, so $d(u, w) = k - 1$. By induction there are two $u$-$w$ paths $P$ and $Q$ with only $u$ and $w$ in common. Since $G - w$ is connected, it has a $u$-$v$ path $R$. Let $z$ be the last vertex of $R$ on $P \cup Q$; it exists because $u$ is on $P$, and say $z \in P$. Then the path $u \xrightarrow{P} z \xrightarrow{R} v$ and the path $u \xrightarrow{Q} w \to v$ have only $u$ and $v$ in common: $R$ after $z$ avoids $P \cup Q$, $R$ avoids $w$, and $P$ and $Q$ meet only at $u$ and $w$. $\square$

**Other equivalent forms** (for $n \ge 3$, and with no isolated vertex for the last one):

- $G$ has an open [ear decomposition](/ear-decomposition/): it is built from a cycle by adding, again and again, a path whose two ends are distinct old vertices and whose inner vertices are new (Diestel, Section 3.1).
- For every two vertices $u \ne v$, at least two vertices must be removed to separate them when they are not adjacent; this is the case $k = 2$ of [Menger's theorem](/menger-theorem/).
- Every two edges lie on a common cycle, so $G$ is a single block.

**Consequences.** A biconnected graph has minimum degree at least 2, so it has at least $n$ edges, and the cycle $C_n$ shows that $n$ edges are enough. It is also [2-edge-connected](/two-edge-connected-graph/), since a [bridge](/bridge/) with $n \ge 3$ has an end that is an articulation point. The converse fails: two triangles that share one vertex are 2-edge-connected but not biconnected.

**Conventions.** Some texts call a connected graph without articulation points *nonseparable* and include $K_1$ and $K_2$, which have no articulation point. With that wording, the blocks of a graph are its maximal nonseparable subgraphs, and the bridges are blocks too. With the definition above, $K_2$ is not biconnected, and in a simple graph the blocks with at least three vertices are the maximal biconnected subgraphs.

**Testing.** Whether $G$ is biconnected is decided in $\Theta(n + m)$ time by one [depth-first search](/depth-first-search/), with the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/): the search must reach all vertices, and no vertex may pass the articulation point test.

## Examples and non-examples

Biconnected:

| graph | why |
|---|---|
| the cycle $C_n$, $n \ge 3$ | two arcs of the cycle join any two vertices |
| the [complete graph](/complete-graph/) $K_n$, $n \ge 3$ | removing a vertex leaves $K_{n-1}$ |
| $K_{2,3}$ | removing a vertex leaves a connected graph; it is a cycle plus one ear |
| the triangle $0, 1, 2$ with a second copy of $\{0, 1\}$ | parallel edges change nothing; the triangle is biconnected |
| the Petersen graph | it is 3-connected, so it is biconnected |

Not biconnected:

| graph | why |
|---|---|
| a path with $n \ge 3$ vertices, or any tree | each inner vertex is an articulation point |
| two triangles sharing one vertex | the shared vertex is an articulation point |
| a cycle with a pendant edge | the end of the pendant edge on the cycle is an articulation point |
| $K_2$, or two vertices with many parallel edges | $n < 3$ |
| a triangle plus an isolated vertex | not connected |

**Small counts.** The number of biconnected simple graphs on the vertex set $\{0, \ldots, n-1\}$ is 1, 10, 238 and 11368 for $n = 3, 4, 5, 6$. Up to isomorphism there are 1, 3, 10 and 56. For $n = 4$, the three are the cycle $C_4$, $C_4$ with one chord, and $K_4$.

## Related definitions

- [Articulation point](/articulation-point/): the vertex that a biconnected graph does not have.
- [Biconnected components](/biconnected-components/) and the [block-cut tree](/block-cut-tree/): how a connected graph splits into biconnected pieces, bridges and loops.
- [k-vertex-connected graph](/k-vertex-connected-graph/): biconnected is the case $k = 2$; the case $k = 3$ is *triconnected*.
- [2-edge-connected graph](/two-edge-connected-graph/): the edge version, a weaker property.
- [Ear decomposition](/ear-decomposition/): the constructive form of the theorem above.
- [st-numbering](/st-numbering/): an order of the vertices that exists for every biconnected graph and every edge $st$, used in planarity testing.

## References
