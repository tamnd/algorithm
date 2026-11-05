---
tag: 657AYN
kind: definition
slug: articulation-point
name: Articulation point
aliases:
- Cut vertex
- Separating vertex
area: graphs/connectivity
level: intro
summary: A vertex whose removal increases the number of connected components.
prereqs: [connected-graph, connected-components]
see_also: [bridge, articulation-point-finding, biconnected-graph, biconnected-components, block-cut-tree, vertex-cut, hopcroft-tarjan-biconnectivity, k-vertex-connected-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (cutvertex and separating sets), and Section 3.1, 2-connected graphs and subgraphs (blocks and the block graph)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2, Paths, cycles, and trails (cut-vertices and cut-edges), and Section 4.1, Cuts and connectivity
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-2, Articulation points, bridges, and biconnected components (Problem 22-2 in the third edition)
---

An articulation point, or cut vertex, of an [undirected graph](/undirected-graph/) is a vertex whose removal, together with its edges, increases the number of [connected components](/connected-components/). In a [connected graph](/connected-graph/), it is a single vertex whose failure splits the graph, like a router that is the only link between two parts of a network. A connected graph with at least three vertices and no articulation point is [biconnected](/biconnected-graph/). All articulation points of a graph can be found in $O(n + m)$ time with one [depth-first search](/depth-first-search/), as the [articulation point finding](/articulation-point-finding/) page shows.

## Definition

Let $G = (V, E)$ be an undirected graph. Parallel edges and [self-loops](/self-loop/) are allowed. For a vertex $v$, let $G - v$ be the graph with the vertex $v$ and all edges at $v$ removed, and let $c(H)$ be the number of components of a graph $H$. Then

$$v \text{ is an articulation point of } G \iff c(G - v) > c(G).$$

Removing $v$ changes only the component $C$ that contains $v$. So $v$ is an articulation point exactly when $C - v$ is not connected. An isolated vertex is never an articulation point: its removal lowers the count by one. Loops and parallel edges never matter, because the definition depends only on which pairs of vertices are adjacent.

**The path form.** The vertex $v$ is an articulation point if and only if there are two vertices $u, w \neq v$ such that $u$ and $w$ are joined by a path in $G$, and every $u$-$w$ path passes through $v$.

*Proof.* Suppose $C - v$ is not connected, and pick $u$ and $w$ in two different components of $C - v$. They are joined by a path in $C$, and every such path avoids $v$ only if it lies in $C - v$, which is impossible. Conversely, if every $u$-$w$ path passes through $v$, then $C - v$ has no $u$-$w$ path, so $C - v$ is not connected. $\square$

**How much the count can grow.** If $v$ has $d$ distinct neighbours, then $c(G - v) \le c(G) - 1 + d$: each component of $C - v$ contains a neighbour of $v$, because a path in $C$ from it to $v$ enters $v$ from a neighbour. The star with $d$ leaves reaches this bound at its centre.

**Facts.** Let $C$ be a component with at least two vertices.

- A vertex with exactly one neighbour is not an articulation point. A path in $C$ between two other vertices $u$ and $w$ that went through $v$ would enter and leave $v$ by two distinct neighbours.
- A leaf of a [spanning tree](/spanning-tree/) $T$ of $C$ is not an articulation point. *Proof.* $T$ minus the leaf is still a tree on all the other vertices of $C$, and it is a subgraph of $C - v$. So $C - v$ is connected. $\square$ Since each tree with at least two vertices has at least two leaves, each connected graph with at least two vertices has at least two vertices that are not articulation points.
- In a [tree](/tree/) with at least three vertices, the articulation points are exactly the vertices of degree at least 2. A vertex with two neighbours $x$ and $y$ in a tree is on the only $x$-$y$ path.
- **Depth-first search.** In a [depth-first forest](/dfs-forest/) of $G$, a root is an articulation point if and only if it has at least two children. A vertex $v$ that is not a root is an articulation point if and only if it has a child $s$ such that no back edge goes from the subtree of $s$ to a proper ancestor of $v$. The [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/) proves this and tests it with [low-link](/low-link/) values.

**Relation to bridges.** If $\{u, v\}$ is a [bridge](/bridge/) and $u$ has a neighbour other than $v$, then $u$ is an articulation point: after the bridge is removed, $v$ and the other neighbour of $u$ are in different components, and every path between them in $G$ uses the bridge and so passes through $u$. The converse fails: two triangles that share one vertex have an articulation point and no bridge.

**Directed graphs.** The term is defined for undirected graphs. For a directed graph, one applies it to the underlying undirected graph, or one asks for a vertex whose removal increases the number of [strongly connected components](/strongly-connected-components/), which is a different notion.

## Examples and non-examples

The graph below has $n = 7$ vertices and 10 edges: a triangle $0, 1, 2$ with the edge $\{0, 1\}$ doubled, the edge $\{2, 3\}$, a triangle $3, 4, 5$, the edge $\{5, 6\}$, and a loop at 6.

| removed vertex $v$ | components of $G - v$ | $c(G - v)$ | articulation point? |
|---|---|---|---|
| none | $\{0, \ldots, 6\}$ | 1 | |
| 0 or 1 | the other six vertices | 1 | no |
| 2 | $\{0, 1\}$, $\{3, 4, 5, 6\}$ | 2 | yes |
| 3 | $\{0, 1, 2\}$, $\{4, 5, 6\}$ | 2 | yes |
| 4 | the other six vertices | 1 | no |
| 5 | $\{0, \ldots, 4\}$, $\{6\}$ | 2 | yes |
| 6 | $\{0, \ldots, 5\}$ | 1 | no |

The articulation points are 2, 3 and 5. The double edge $\{0, 1\}$ and the loop at 6 change nothing. The vertex 6 has one neighbour, so it is not an articulation point, although its loop gives it degree 3.

More cases:

| graph | articulation points |
|---|---|
| the path $0 - 1 - 2 - 3$ | 1 and 2 |
| the star with centre 0 and leaves 1 to 4 | 0; removing it leaves 4 components |
| a cycle | none |
| two triangles sharing the vertex 0 | 0, and the graph has no bridge |
| a single edge $\{0, 1\}$ | none, although the edge is a bridge |
| a single vertex | none |
| a [complete graph](/complete-graph/) | none |

## Related definitions

- [Bridge](/bridge/): the same idea for an edge.
- [Vertex cut](/vertex-cut/): a set of vertices whose removal disconnects the graph. An articulation point is a vertex cut of size 1.
- [Biconnected graph](/biconnected-graph/): a connected graph with at least three vertices and no articulation point.
- [Biconnected components](/biconnected-components/): the blocks, which meet only at articulation points.
- [Block-cut tree](/block-cut-tree/): the tree of the blocks and the articulation points.
- [k-vertex-connected graph](/k-vertex-connected-graph/): no set of fewer than $k$ vertices disconnects the graph.
- [Articulation point finding](/articulation-point-finding/): the problem of listing all of them.

## References
