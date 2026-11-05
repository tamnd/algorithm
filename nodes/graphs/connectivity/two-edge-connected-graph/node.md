---
tag: 72GHJ2
kind: definition
slug: two-edge-connected-graph
name: 2-edge-connected graph
aliases:
- Bridgeless connected graph
area: graphs/connectivity
level: core
summary: A connected graph with no bridge.
prereqs: [connected-graph, bridge, simple-cycle]
see_also: [two-edge-connected-components, k-edge-connected-graph, edge-connectivity, biconnected-graph, strong-orientation, ear-decomposition, bridge-finding, menger-theorem]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2, Paths, cycles, and trails (an edge is a cut-edge exactly when it lies on no cycle); Section 4.1, Cuts and connectivity (k-edge-connected graphs); Section 4.2, k-connected graphs (closed-ear decompositions of 2-edge-connected graphs, and Robbins' theorem)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (bridges and k-edge-connected graphs)
  - paper: doi:10.2307/2303897
    title: H. E. Robbins, A theorem on graphs, with an application to a problem of traffic control, American Mathematical Monthly 46(5), 281 to 283 (1939)
    locator: the whole paper (a graph has a strongly connected orientation exactly when it is connected and has no bridge)
---

A 2-edge-connected graph is a [connected](/connected-graph/) undirected graph in which no single edge is a [bridge](/bridge/): removing any one edge leaves it connected. Equivalently, every edge lies on a [cycle](/simple-cycle/), and any two vertices are joined by two paths that share no edge. These are exactly the graphs whose roads can all be made one-way so that every place can still reach every other, by Robbins' theorem on [strong orientations](/strong-orientation/).

## Definition

Let $G = (V, E)$ be an undirected graph. [Parallel edges](/multigraph/) and [self-loops](/self-loop/) are allowed, and two parallel copies of an edge count as different edges. An edge $e$ is a *bridge* if $G - e$ has more [connected components](/connected-components/) than $G$.

$G$ is *2-edge-connected* if it is connected and has no bridge.

**Small cases.** By this definition the graph with one vertex is 2-edge-connected, with or without loops. Some books, such as West, ask a $k$-edge-connected graph to have at least 2 vertices, which excludes it; the alias "bridgeless connected graph" includes it. The graph with 2 vertices and one edge is not 2-edge-connected, but with two parallel edges it is.

### Equivalent forms

**Proposition.** For a connected undirected graph $G$, the following are equivalent.

1. $G$ has no bridge.
2. Every edge of $G$ lies on a cycle.
3. For any two vertices $u$ and $v$, $G$ has two edge-disjoint $u$-$v$ paths.
4. $G$ has an orientation that is [strongly connected](/strongly-connected-graph/).

Here a loop is a cycle of length 1, and two parallel edges form a cycle of length 2.

*Proof of 1 ⇔ 2.* We show that an edge $e = \{u, v\}$ is a bridge exactly when it lies on no cycle. A loop lies on a cycle and is never a bridge, as removing it does not change which vertices are joined; so let $u \ne v$. If $e$ lies on a cycle $C$, then $C - e$ is a $u$-$v$ path in $G - e$. Any walk in $G$ that uses $e$ can use this path instead, so $G - e$ has the same components as $G$, and $e$ is not a bridge. If $e$ lies on no cycle, then $G - e$ has no $u$-$v$ path, because such a path together with $e$ would be a cycle. So $u$ and $v$ are in one component of $G$ and in two components of $G - e$; no other vertex changes component, as each one joined to $u$ or $v$ in $G$ is still joined to one of them, so $G - e$ has one more component, and $e$ is a bridge. $\square$

*Proof of 1 ⇔ 3.* If $G$ has a bridge $e = \{u, v\}$, every $u$-$v$ path uses $e$, so there are no two edge-disjoint ones. Conversely, if $G$ has no bridge, then for $u \ne v$, removing any one edge leaves a $u$-$v$ path, so the least number of edges that meet every $u$-$v$ path is at least 2, and the edge form of [Menger's theorem](/menger-theorem/) gives two edge-disjoint $u$-$v$ paths. For $u = v$, take the path of length 0 twice. $\square$

*Proof of 1 ⇔ 4.* If an orientation is strongly connected and $e = \{u, v\}$ is oriented from $u$ to $v$, a directed path from $v$ back to $u$ does not use $e$, so it closes a cycle with $e$, and $e$ is not a bridge by 1 ⇔ 2. The converse is Robbins' theorem; the proof by depth-first search is on the [strong orientation](/strong-orientation/) page. $\square$

Two more criteria are useful.

- **DFS criterion.** Run a [depth-first search](/depth-first-search/) of $G$ from any vertex. $G$ is 2-edge-connected exactly when the search reaches every vertex and every non-root vertex $c$ has $\mathrm{low}[c] \le d[p]$, where $p$ is the parent of $c$ and $\mathrm{low}$ is the [low point](/low-link/). This follows from the bridge criterion $\mathrm{low}[c] > d[p]$ on that page, and gives a $\Theta(n + m)$ test.
- **Ears.** $G$ is 2-edge-connected exactly when it has a *closed-ear decomposition*: it is built from one cycle by adding, one at a time, paths whose two ends are already in the graph, or cycles through one vertex already in the graph. West proves this in Section 4.2; see [ear decomposition](/ear-decomposition/).

## Examples and non-examples

- **Cycles and complete graphs.** Every cycle $C_n$ with $n \ge 3$, and every $K_n$ with $n \ge 3$, is 2-edge-connected.
- **Small simple graphs.** On 4 vertices, exactly three simple graphs are 2-edge-connected, up to isomorphism: $C_4$, $K_4$ minus an edge, and $K_4$. Every other connected simple graph on 4 vertices has a vertex of degree 1, whose edge is a bridge.
- **Bowtie.** Two triangles that share one vertex form a 2-edge-connected graph that is not [biconnected](/biconnected-graph/): the shared vertex is an [articulation point](/articulation-point/), but every edge lies on a triangle.
- **Multigraph.** Two vertices joined by two parallel edges form a 2-edge-connected graph. Doubling every edge of any connected graph makes it 2-edge-connected.
- **Petersen graph.** It is 3-edge-connected, so in particular 2-edge-connected.
- **Non-example: trees.** In a [tree](/tree/) with at least 2 vertices every edge is a bridge.
- **Non-example: dumbbell.** Two triangles joined by one edge: that edge is a bridge, although every vertex has degree at least 2. Minimum degree 2 is necessary but not enough.
- **Non-example: disconnected.** Two disjoint triangles have no bridge but are not connected, so they are not 2-edge-connected. Each triangle is a [2-edge-connected component](/two-edge-connected-components/).
- **Loops do not help.** A path $a - b$ with a loop at $a$ and one at $b$ still has the bridge $\{a, b\}$.

## Related definitions

- [Bridge](/bridge/): an edge whose removal disconnects; a 2-edge-connected graph is a connected graph with none.
- [$k$-edge-connected graph](/k-edge-connected-graph/) and [edge connectivity](/edge-connectivity/): 2-edge-connected means $\lambda(G) \ge 2$ (for at least 2 vertices).
- [Biconnected graph](/biconnected-graph/): no [articulation point](/articulation-point/). With at least 3 vertices, a biconnected graph is 2-edge-connected, because each edge lies on a cycle; the bowtie shows the converse fails.
- [Two-edge-connected components](/two-edge-connected-components/): the maximal 2-edge-connected subgraphs, found by removing all bridges.
- [Strong orientation](/strong-orientation/): an orientation that is strongly connected; it exists exactly for 2-edge-connected graphs.
- For directed graphs, a *2-edge-connected digraph* is one that stays [strongly connected](/strongly-connected-graph/) after the removal of any one arc. That is a different and harder notion.

## References
