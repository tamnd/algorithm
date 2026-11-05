---
tag: QAACP7
kind: concept
slug: spanning-forest
name: Spanning forest
aliases:
- maximal forest
area: graphs/spanning-trees
level: intro
summary: A spanning subgraph of a disconnected graph whose components are spanning trees.
prereqs: [spanning-tree, connected-components, tree-edge-count]
see_also: [kruskal, graphic-matroid, union-find-connectivity, dynamic-connectivity, nagamochi-ibaraki-certificate, cycle-basis, arboricity, minimum-spanning-tree]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition
    locator: Section 1.5, Trees and forests (forests, spanning trees of the components) and Section 1.9, Some linear algebra (the cycle space has dimension m - n + c)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 2.1, Basic properties of trees (a forest with n vertices and k components has n - k edges)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5.1, Free trees (forests), and Chapter 21, Minimum Spanning Trees (Kruskal's algorithm grows a forest)
---

A spanning forest of an undirected graph $G$ is a set of edges that has no cycle and has the same [connected components](/connected-components/) as $G$: inside each component of $G$ it is a [spanning tree](/spanning-tree/) of that component. Each finite graph has one, and it has exactly $n - c$ edges when $G$ has $n$ vertices and $c$ components. It is the right output for algorithms such as [Kruskal's algorithm](/kruskal/) when the input graph need not be [connected](/connected-graph/), and it is the basis of the [graphic matroid](/graphic-matroid/).

## In plain words

A spanning tree connects all the vertices of a graph with no loop. If the graph is in several pieces that no edge joins, no tree can reach all the vertices. The best you can do is to pick a tree inside each piece. The trees together are a spanning forest.

A spanning forest keeps the same connections as the graph. Two vertices are joined by forest edges exactly when they are joined by graph edges. It uses as few edges as possible for that: one fewer than the number of vertices in each piece. If you add any other edge of the graph to it, you close a loop.

Many programs on graphs build one: a search from each vertex that is not yet reached gives a tree for each piece.

## The idea

Let $G = (V, E)$ be a finite undirected graph, with $n = |V|$ vertices, $m = |E|$ edges and $c$ connected components $V_1, \ldots, V_c$. A *forest* is a set $F \subseteq E$ such that $(V, F)$ has no cycle. Parallel edges and self-loops are allowed in $G$, and the graph need not be connected.

**Definition.** A **spanning forest** of $G$ is a forest $F \subseteq E$ such that, for each two vertices $u, v$, there is a path from $u$ to $v$ in $(V, F)$ if and only if there is one in $G$.

Some authors use "spanning forest" for any forest $F \subseteq E$ on the vertex set $V$, even the empty set, and say *maximal spanning forest* for the object defined here. This site uses the stronger meaning above. The alias "maximal forest" comes from the next fact.

**Three equivalent conditions.** For a forest $F \subseteq E$, these are equivalent:

1. $F$ is a spanning forest.
2. $F$ is a maximal forest: for each $e \in E \setminus F$, the set $F \cup \{e\}$ has a cycle.
3. $|F| = n - c$.

*Proof.* A forest whose graph has $k$ components has $n - k$ edges, because a tree on $n_i$ vertices has $n_i - 1$ edges ([tree edge count](/tree-edge-count/)) and the sum of $n_i - 1$ over the $k$ trees is $n - k$. Each component of $(V, F)$ lies inside a component of $G$, since $F \subseteq E$, so $k \ge c$.

(1) implies (3): the components of $(V, F)$ are those of $G$, so $k = c$ and $|F| = n - c$.

(3) implies (1): $|F| = n - k = n - c$ gives $k = c$. Each of the $c$ components of $G$ holds at least one component of $(V, F)$, and there are only $c$ of them, so each component of $G$ holds exactly one. So the components are the same.

(1) implies (2): let $e = uv \in E \setminus F$. Then $u$ and $v$ are in one component of $G$, so $(V, F)$ has a path from $u$ to $v$, and this path with $e$ is a cycle.

(2) implies (1): suppose that $F$ is maximal but some $u, v$ are joined in $G$ and not in $(V, F)$. Take a path from $u$ to $v$ in $G$. Its first vertex is in the tree of $u$ and its last vertex is not, so one of its edges $e$ joins two different trees of $F$. Then $F \cup \{e\}$ has no cycle, which contradicts maximality. $\square$

**Existence and construction.** Take a spanning tree of each component, or run a [graph traversal](/graph-traversal/) from each vertex that is not yet reached and keep the edge by which each vertex is first reached. A [breadth-first](/breadth-first-search/) or [depth-first search](/depth-first-search/) of the whole graph does this in $O(n + m)$ time. Kruskal's test "do the two ends lie in different trees" with a [disjoint-set](/disjoint-set/) structure also builds one, edge by edge, in any order of the edges.

**Two numbers.** The size $n - c$ of each spanning forest is the rank of the graphic matroid. The number $m - (n - c) = m - n + c$ of edges outside a spanning forest is the dimension of the cycle space of $G$ over the field with two elements: each edge outside $F$ closes one [fundamental cycle](/fundamental-cycle/), and these cycles form a [cycle basis](/cycle-basis/).

**Weights.** When the edges have real weights, a *minimum spanning forest* is a spanning forest of least total weight. It is the union of a [minimum spanning tree](/minimum-spanning-tree/) of each component. Weights may be negative and may tie; with ties, more than one minimum spanning forest can exist.

## Examples

**A graph in three pieces.** Let $V = \{1, \ldots, 6\}$ and $E = \{12, 23, 13, 45\}$. The components are $\{1, 2, 3\}$, $\{4, 5\}$ and $\{6\}$, so $n = 6$, $c = 3$, and each spanning forest has $6 - 3 = 3$ edges. The forest must hold $45$, no edge at $6$, and two of the three edges of the triangle. So there are exactly 3 spanning forests: $\{12, 23, 45\}$, $\{12, 13, 45\}$ and $\{23, 13, 45\}$. The number $m - n + c = 4 - 6 + 3 = 1$ counts the one independent cycle, the triangle.

**Counting.** In general, the number of spanning forests is the product of the numbers of spanning trees of the components. For two disjoint copies of $K_4$, it is $16 \cdot 16 = 256$.

**Non-examples in the same graph.**

- $\{12, 45\}$ is a forest, but $3$ is not joined to $1$ in it, and adding $23$ closes no cycle. It is not maximal, and it has $2 \ne 3$ edges.
- $\{12, 23, 13\}$ has 3 edges, but it has a cycle, so it is not a forest.
- The empty set is a spanning forest only when $G$ has no edges except self-loops.

**A connected graph.** When $c = 1$, a spanning forest is exactly a spanning tree. So "spanning forest" is the general notion, and code that returns a spanning forest is correct on both kinds of input.

## Where it is used

- [Kruskal's algorithm](/kruskal/) and [Borůvka's algorithm](/boruvka/) return a minimum spanning forest when the graph is not connected, with no change to the code.
- [Connectivity with union-find](/union-find-connectivity/): the union operations that merge two sets are exactly the edges of a spanning forest of the edges seen so far.
- [Dynamic connectivity](/dynamic-connectivity/): the structure of [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/) keeps a spanning forest and looks for a replacement edge when a forest edge is deleted.
- Sparse certificates: the [Nagamochi-Ibaraki certificate](/nagamochi-ibaraki-certificate/) takes $F_1$ a spanning forest of $G$, $F_2$ a spanning forest of $G \setminus F_1$, and so on. The union of $F_1, \ldots, F_k$ has at most $k(n - 1)$ edges and keeps all edge cuts of size less than $k$.
- [Cycle bases](/cycle-basis/): the fundamental cycles of the edges outside a spanning forest form a basis of the cycle space.
- [Arboricity](/arboricity/): the least number of forests that cover all edges of a graph.
- The [graphic matroid](/graphic-matroid/): its bases are the spanning forests, and its rank is $n - c$.

## References
