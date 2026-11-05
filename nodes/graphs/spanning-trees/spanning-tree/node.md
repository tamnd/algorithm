---
tag: DH4X7X
kind: definition
slug: spanning-tree
name: Spanning tree
aliases:
- spanning subtree
area: graphs/spanning-trees
level: intro
summary: An acyclic connected subgraph that contains every vertex of a connected graph.
prereqs: [undirected-graph, subgraph, tree, connected-graph]
see_also: [spanning-forest, minimum-spanning-tree, free-tree-properties, fundamental-cycle, counting-spanning-trees, matrix-tree-theorem, graphic-matroid, arborescence]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5.1, Free trees (Theorem B.2, the equivalent conditions for a tree), and Chapter 21, Minimum Spanning Trees (the spanning tree of a connected graph)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 2.1, Basic properties of trees (spanning trees and the characterizations of trees), and Section 2.2, Spanning trees and enumeration
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition
    locator: Section 1.5, Trees and forests (the equivalent definitions of a tree and the existence of a spanning tree in each connected graph)
---

A spanning tree of a connected [undirected graph](/undirected-graph/) $G$ is a [subgraph](/subgraph/) that contains every vertex of $G$ and is a [tree](/tree/): it is connected and has no cycle. It has exactly $n - 1$ edges when $G$ has $n$ vertices. A graph has a spanning tree if and only if it is [connected](/connected-graph/), and a graph that is not connected has a [spanning forest](/spanning-forest/) instead. Spanning trees are the objects of the [minimum spanning tree problem](/minimum-spanning-tree/), and each graph search, such as [breadth-first search](/breadth-first-search/) or [depth-first search](/depth-first-search/), builds one.

## Definition

Let $G = (V, E)$ be a finite undirected graph with $n = |V| \ge 1$ vertices and $m = |E|$ edges. Parallel edges and [self-loops](/self-loop/) are allowed. A **spanning tree** of $G$ is a set of edges $T \subseteq E$ such that the graph $(V, T)$ is a tree, that is, $(V, T)$ is connected and has no cycle. Some authors call the subgraph $(V, T)$ the spanning tree. The two uses name the same object, because the vertex set is always all of $V$.

For a set $T \subseteq E$, the following conditions are equivalent ([free tree properties](/free-tree-properties/), CLRS Theorem B.2):

1. $(V, T)$ is connected and acyclic.
2. $(V, T)$ is connected and $|T| = n - 1$.
3. $(V, T)$ is acyclic and $|T| = n - 1$.
4. For each two vertices $u, v \in V$, $(V, T)$ has exactly one simple path from $u$ to $v$.
5. $(V, T)$ is connected, and $(V, T \setminus \{e\})$ is not connected for each $e \in T$ (a minimal connected spanning subgraph).
6. $(V, T)$ is acyclic, and $(V, T \cup \{e\})$ has a cycle for each $e \in E \setminus T$ (a maximal acyclic subgraph of $G$, when $G$ is connected).

A self-loop is a cycle of length 1, so it is never in a spanning tree. Two parallel edges form a cycle of length 2, so a spanning tree holds at most one edge of each parallel class. When the edges carry weights, the definition does not use them. Ties in the weights matter only for the [minimum spanning tree](/minimum-spanning-tree/), where they can make the minimum tree not unique.

**Existence.** $G$ has a spanning tree if and only if $G$ is connected. If $(V, T)$ is a spanning tree, it is connected, and $T \subseteq E$, so $G$ is connected. Conversely, let $G$ be connected. Start with $T = E$. While $(V, T)$ has a cycle, remove one edge of the cycle. The two ends of the removed edge stay joined by the rest of the cycle, so each path that used the edge can go around it, and $(V, T)$ stays connected. Each step removes one edge, so the process stops after at most $m$ steps, with a connected acyclic graph. The same argument with an empty start and "add an edge that joins two components" gives the other standard proof.

**Directed graphs.** In a directed graph, the analogue is a spanning [arborescence](/arborescence/): a set of arcs in which each vertex except a root $r$ has exactly one entering arc, and each vertex is reachable from $r$.

## Examples and non-examples

The table gives the number $\tau(G)$ of spanning trees of some small graphs. The [matrix-tree theorem](/matrix-tree-theorem/) computes each value as a determinant.

| graph $G$ | $n$ | $m$ | $\tau(G)$ |
|---|---|---|---|
| a tree | $n$ | $n - 1$ | 1, the tree itself |
| the cycle $C_5$ | 5 | 5 | 5: delete any one edge |
| the square with one diagonal | 4 | 5 | 8 |
| the complete graph $K_4$ | 4 | 6 | 16 |
| the complete bipartite graph $K_{2,3}$ | 5 | 6 | 12 |
| the Petersen graph | 10 | 15 | 2000 |

For the complete graph, $\tau(K_n) = n^{n-2}$ by [Cayley's formula](/cayley-formula/), so $\tau(K_4) = 16$. For the complete bipartite graph, $\tau(K_{a,b}) = a^{b-1} b^{a-1}$, so $\tau(K_{2,3}) = 2^2 \cdot 3 = 12$.

**Example: the square with a diagonal.** Take $V = \{1, 2, 3, 4\}$ and $E = \{12, 23, 34, 41, 13\}$. A spanning tree has $3$ of the $5$ edges, and there are $\binom{5}{3} = 10$ sets of 3 edges. A set of 3 edges fails only when it is a triangle: $\{12, 23, 13\}$ and $\{34, 41, 13\}$. So $10 - 2 = 8$ sets are spanning trees. For example, $\{12, 23, 34\}$ is a Hamiltonian path, and $\{12, 13, 34\}$ is the path 2, 1, 3, 4. A spanning tree need not be a path: $\{12, 13, 14\}$ is a star with center 1.

**Spanning trees made by search.** A [BFS tree](/bfs-tree/) from a vertex $s$ of a connected graph is a spanning tree in which the path from $s$ to each vertex is a shortest path in the number of edges. A [DFS forest](/dfs-forest/) of a connected graph is a single spanning tree. A [shortest-path tree](/shortest-path-tree/) of a weighted graph is also a spanning tree. Each Hamiltonian path is a spanning tree with maximum degree 2.

**Non-examples.**

- In the square with a diagonal, $\{12, 23, 13\}$ has $n - 1 = 3$ edges but is not a spanning tree. It has a cycle, and the vertex 4 is not reached. This shows that "$n - 1$ edges" alone is not enough: the set must also be connected or acyclic.
- $\{12, 23\}$ is a tree, but it misses vertex 4, so it is not spanning.
- $\{12, 23, 34, 41\}$ is connected and spans, but it has a cycle and $4 > n - 1$ edges.
- A graph that is not connected, such as two disjoint edges, has no spanning tree at all. Its maximal acyclic subgraphs are spanning forests.

## Related definitions

- [Tree](/tree/) and [free tree properties](/free-tree-properties/): the equivalent conditions used above, and the [tree edge count](/tree-edge-count/) $n - 1$.
- [Spanning forest](/spanning-forest/): the version for a graph that may be disconnected, with $n - c$ edges for $c$ components.
- [Fundamental cycle](/fundamental-cycle/): adding one non-tree edge to a spanning tree closes exactly one cycle. This is condition 6 in a stronger form.
- [Minimum spanning tree](/minimum-spanning-tree/): a spanning tree of least total weight.
- [Counting spanning trees](/counting-spanning-trees/), the [matrix-tree theorem](/matrix-tree-theorem/) and [Cayley's formula](/cayley-formula/) count them, and [spanning tree enumeration](/spanning-tree-enumeration/) lists them.
- [Graphic matroid](/graphic-matroid/): the spanning trees of a connected graph are the bases of this matroid. The [spanning tree polytope](/spanning-tree-polytope/) is the convex hull of their incidence vectors.
- [Arborescence](/arborescence/): the directed analogue, with a root.

## References
