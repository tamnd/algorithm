---
tag: Y4395F
kind: definition
slug: vertex-cut
name: Vertex cut
aliases:
- Separating set
- Node cut
area: graphs/connectivity
level: core
summary: A set of vertices whose removal disconnects two given vertices or the graph.
prereqs: [connected-graph, connected-components]
see_also: [articulation-point, vertex-connectivity, k-vertex-connected-graph, menger-theorem, cut, edge-connectivity, vertex-disjoint-paths, planar-separator-theorem]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.1, Cuts and connectivity (separating sets, connectivity, the convention for complete graphs, and the inequality between vertex connectivity, edge connectivity and minimum degree)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (sets that separate two sets of vertices, k-connected graphs, and the bound of connectivity by edge connectivity and minimum degree)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Springer Graduate Texts in Mathematics 244
    locator: Chapter 9, Connectivity (vertex cuts and connectivity)
---

A vertex cut of a graph is a set of vertices whose removal leaves the graph disconnected. For two given vertices $s$ and $t$, an $s$-$t$ vertex cut is a set of other vertices that meets every path from $s$ to $t$. The least size of a vertex cut is the [vertex connectivity](/vertex-connectivity/) of the graph, and [Menger's theorem](/menger-theorem/) says that the least size of an $s$-$t$ vertex cut equals the largest number of $s$-$t$ paths that share no inner vertex.

## Definition

Let $G = (V, E)$ be a graph with $n$ vertices. It may be undirected or directed, and it may have [parallel edges](/multigraph/) and [self-loops](/self-loop/). Neither changes anything on this page, because a path never uses a loop or a second copy of an edge, and the removal of a vertex removes all its edges. For $S \subseteq V$, write $G - S$ for the graph left when the vertices of $S$ and all edges at them are removed.

**$s$-$t$ vertex cut.** Let $s \ne t$ be vertices such that $G$ has no edge from $s$ to $t$ (in a directed graph, no arc $(s, t)$). A set $S \subseteq V \setminus \{s, t\}$ is an *$s$-$t$ vertex cut*, or *$s$-$t$ separator*, if $G - S$ has no path from $s$ to $t$. In a directed graph the paths are directed paths. The least size of an $s$-$t$ vertex cut is written $\kappa(s, t)$.

If $s$ and $t$ are adjacent, no $s$-$t$ vertex cut exists, because the edge $st$ survives the removal of any set that avoids $s$ and $t$. This is why the definition excludes this case.

**Vertex cut of a graph.** A set $S \subseteq V$ is a *vertex cut*, or *separating set*, of $G$ if $G - S$ is disconnected. For a directed graph, "disconnected" means "not [strongly connected](/strongly-connected-graph/)". A graph with fewer than 2 vertices, and a single vertex, count as connected, so $G - S$ must keep at least 2 vertices.

**Minimal and minimum.** A vertex cut is *minimal* if no proper subset of it is a vertex cut, and *minimum* if no vertex cut is smaller. Every minimum cut is minimal, and the converse fails (see the examples).

**Connectivity.** The *vertex connectivity* $\kappa(G)$ is the least size of a vertex cut of $G$. A [complete graph](/complete-graph/) $K_n$ has no vertex cut, as every set it leaves is again complete, and the usual convention sets $\kappa(K_n) = n - 1$. With this convention, $\kappa(G) \ge k$ exactly when $G$ is [$k$-vertex-connected](/k-vertex-connected-graph/). A vertex cut of size 1 is an [articulation point](/articulation-point/).

### Basic facts

**Fact 1 (local and global).** If $G$ is not complete, then $\kappa(G) = \min \kappa(s, t)$ over all pairs of distinct non-adjacent vertices $s, t$. *Proof.* An $s$-$t$ vertex cut $S$ is a vertex cut of $G$, because $s$ and $t$ survive and are not joined in $G - S$. Conversely, if $G - S$ is disconnected, take $s$ and $t$ in different parts of $G - S$ (in the directed case, with no path from $s$ to $t$ in $G - S$). They are not adjacent, and $S$ is an $s$-$t$ vertex cut. $\square$

**Fact 2 (minimal cuts are full).** Let $G$ be undirected and $S$ a minimal vertex cut. Then every vertex of $S$ has a neighbour in every component of $G - S$. *Proof.* Suppose $x \in S$ has no neighbour in a component $A$ of $G - S$. In $G - (S \setminus \{x\})$, no edge leaves $A$, and there are vertices outside $A$ (at least $x$ and the other components), so $S \setminus \{x\}$ is also a vertex cut. This contradicts minimality. $\square$ For the same reason, a minimal $s$-$t$ vertex cut has every vertex adjacent to the component of $s$ and to the component of $t$ in $G - S$.

**Fact 3 (Whitney's inequality).** Let $G$ be undirected with $n \ge 2$ vertices, let $\lambda(G)$ be its [edge connectivity](/edge-connectivity/), the least number of edges whose removal disconnects it, and let $\delta(G)$ be its least degree, with loops not counted. Then $\kappa(G) \le \lambda(G) \le \delta(G)$.

*Proof.* Removing all non-loop edges at a vertex of degree $\delta$ cuts it off, so $\lambda \le \delta$. For $\kappa \le \lambda$, let $F$ be a set of $\lambda$ edges whose removal disconnects $G$. Then $V$ splits into nonempty sets $X$ and $Y$ such that every edge between $X$ and $Y$ is in $F$. If every vertex of $X$ is adjacent to every vertex of $Y$, then $\lambda = |F| \ge |X| \cdot |Y| \ge n - 1 \ge \kappa(G)$, since $\kappa \le n - 1$ always. Else take $x \in X$ and $y \in Y$ not adjacent. For each edge $ab \in F$ with $a \in X$ and $b \in Y$, put $a$ in $S$ if $a \ne x$, and $b$ in $S$ if $a = x$; then $b \ne y$, as $x$ and $y$ are not adjacent. So $S$ avoids $x$ and $y$ and $|S| \le |F|$. Every $x$-$y$ path uses an edge between $X$ and $Y$, which is in $F$, and contains both its ends, so it meets $S$. So $S$ is an $x$-$y$ vertex cut and $\kappa(G) \le |S| \le \lambda(G)$. $\square$

## Examples and non-examples

- **Path.** In the path $a - b - c$, the set $\{b\}$ is a vertex cut, and $b$ is an articulation point. $\kappa = 1$.
- **Cycle.** In a cycle $C_n$ with $n \ge 4$, any two non-adjacent vertices form a vertex cut, and no single vertex does, so $\kappa(C_n) = 2$.
- **Complete bipartite graph.** In $K_{p,q}$ with $2 \le p \le q$, each side is a vertex cut, as removing it leaves the other side with no edges. $\kappa(K_{p,q}) = p$.
- **Petersen graph.** The 3 neighbours of any vertex form a vertex cut, and no 2 vertices do, so $\kappa = 3$.
- **Minimal but not minimum.** In the cycle $0 - 1 - 2 - 3 - 4 - 5 - 0$ with an extra vertex 6 joined to 0 and to 3, the set $\{1, 4, 6\}$ is a minimal vertex cut: removing it leaves the parts $\{2, 3\}$ and $\{5, 0\}$, and putting back any one of its vertices joins them again. The minimum vertex cuts, such as $\{0, 2\}$, have size 2.
- **Strict inequalities.** Take two copies of $K_4$, on $\{0, 1, 2, 3\}$ and $\{4, 5, 6, 7\}$, and add the edges $\{0, 4\}$ and $\{0, 5\}$. Then $\kappa = 1$ (vertex 0), $\lambda = 2$ (the two added edges), and $\delta = 3$. So both inequalities of Fact 3 can be strict.
- **Directed.** With the arcs $s \to a \to t$, $s \to b \to t$ and $t \to s$, the set $\{a, b\}$ is an $s$-$t$ vertex cut. The arc $t \to s$ does not matter, because only paths from $s$ to $t$ count.
- **Parallel edges and loops.** Doubling every edge of a graph, or adding loops, changes no vertex cut. It does change $\lambda$, which counts edges with multiplicity: a doubled path $a = b = c$ still has $\kappa = 1$ but has $\lambda = 2$.
- **Non-example: complete graph.** In $K_n$, removing any $n - 2$ vertices leaves an edge, and removing $n - 1$ leaves one vertex; both are connected. So $K_n$ has no vertex cut.
- **Non-example: adjacent ends.** For an edge $st$, no set of other vertices separates $s$ from $t$.
- **Empty cut.** If $G$ is already disconnected, the empty set is a vertex cut and $\kappa(G) = 0$.

## Related definitions

- [Articulation point](/articulation-point/): a vertex cut of size 1 in a connected graph.
- [Vertex connectivity](/vertex-connectivity/) and [$k$-vertex-connected graph](/k-vertex-connected-graph/): the least size of a vertex cut, and the graphs where it is at least $k$.
- [Edge cut](/cut/) and [edge connectivity](/edge-connectivity/): the same ideas with edges instead of vertices.
- [Menger's theorem](/menger-theorem/): $\kappa(s, t)$ equals the largest number of [internally vertex-disjoint](/vertex-disjoint-paths/) $s$-$t$ paths.
- [Planar separator theorem](/planar-separator-theorem/): a *balanced separator* is a vertex cut whose removal leaves parts of bounded size, which is a different aim from a small cut between two given vertices.
- [Block-cut tree](/block-cut-tree/): the structure of the vertex cuts of size 1.

## References
