---
tag: 6TN2Z8
kind: definition
slug: k-edge-connected-graph
name: k-edge-connected graph
aliases:
- k-edge-connected
area: graphs/connectivity
level: advanced
summary: A graph that stays connected after removing any fewer than k edges.
prereqs: [connected-graph, bridge]
see_also: [edge-connectivity, k-vertex-connected-graph, two-edge-connected-graph, menger-theorem, nagamochi-ibaraki-certificate, ear-decomposition, strong-orientation, cut]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (the definition of l-edge-connected and of the edge-connectivity), and Section 3.3, Menger's theorem (the edge version)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.1, Cuts and connectivity (edge cuts and k-edge-connected graphs), and Section 4.2, k-connected graphs (Menger's theorem for edges)
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert E. Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: testing edge connectivity with maximum flows on unit capacities
---

A graph is $k$-edge-connected if it has at least two vertices and stays [connected](/connected-graph/) whenever fewer than $k$ edges are removed. The largest such $k$ is the [edge connectivity](/edge-connectivity/) $\lambda(G)$. A graph is 1-edge-connected when it is connected, and 2-edge-connected when it is connected and has no [bridge](/bridge/). By [Menger's theorem](/menger-theorem/), $k$-edge-connected means that every two vertices are joined by $k$ paths with no edge in common, so a network with this property survives the failure of any $k - 1$ links.

## Definition

Let $G = (V, E)$ be an undirected graph with $n = |V|$. $E$ is a multiset: parallel edges count with their multiplicity, and [self-loops](/self-loop/) are allowed but play no part, since removing a loop never disconnects anything. Let $k \ge 0$ be an integer.

$G$ is **$k$-edge-connected** if $n \ge 2$ and $G - F$ is connected for every set $F \subseteq E$ with $|F| < k$.

For a set $S \subseteq V$, the *cut* $\delta(S)$ is the set of edges with one end in $S$ and one end outside $S$ (see [cut](/cut/)). Loops are never in a cut.

**Equivalent forms.** For $n \ge 2$ and $k \ge 1$, these are equivalent:

1. $G$ is $k$-edge-connected.
2. $|\delta(S)| \ge k$ for every $S$ with $\emptyset \neq S \subsetneq V$.
3. Every two distinct vertices are joined by $k$ paths that are pairwise edge-disjoint.

*Proof of 1 ⇔ 2.* If $|\delta(S)| < k$ for some proper non-empty $S$, then $F = \delta(S)$ has fewer than $k$ edges and $G - F$ has no edge between $S$ and $V \setminus S$, so it is not connected. Conversely, if $G - F$ is not connected for some $|F| < k$, let $S$ be the vertex set of one of its components. Then $\delta(S) \subseteq F$, so $|\delta(S)| < k$. $\square$

The equivalence with 3 is the edge version of Menger's theorem (Diestel, Section 3.3). One direction is short: $k$ edge-disjoint $u$-$v$ paths each use an edge of every cut that separates $u$ from $v$, so such a cut has at least $k$ edges.

**Edge connectivity.** $\lambda(G)$ is the largest $k$ such that $G$ is $k$-edge-connected, and $\lambda(G) = \min \{ |\delta(S)| : \emptyset \neq S \subsetneq V \}$ by form 2. So $G$ is $k$-edge-connected exactly when $\lambda(G) \ge k$, and every $k$-edge-connected graph is also $j$-edge-connected for $j < k$.

**Basic facts.**

- **Degree.** Taking $S = \{v\}$ gives $\deg(v) \ge k$ (loops not counted), so the minimum degree is at least $k$ and $G$ has at least $kn/2$ edges that are not loops. A $k$-regular $k$-edge-connected graph, such as a cycle for $k = 2$, meets this bound.
- **Vertex connectivity.** Whitney's inequality $\kappa(G) \le \lambda(G) \le \delta(G)$ holds; see [edge connectivity](/edge-connectivity/). So every [$k$-vertex-connected graph](/k-vertex-connected-graph/) is $k$-edge-connected. The converse fails: two triangles that share a vertex are 2-edge-connected but only 1-vertex-connected.
- **Gluing.** If $G_1$ and $G_2$ are $k$-edge-connected and share at least one vertex, their union is $k$-edge-connected. Removing fewer than $k$ edges leaves each $G_i$ connected, and the shared vertex joins the two.
- **Small $k$.** Every graph with $n \ge 2$ is 0-edge-connected. $G$ is 1-edge-connected if and only if it is connected, and [2-edge-connected](/two-edge-connected-graph/) if and only if it is connected and has no bridge, which holds if and only if it has an [ear decomposition](/ear-decomposition/).
- **Parallel edges.** Two vertices joined by $k$ parallel edges form a $k$-edge-connected graph. In a simple graph, $k$-edge-connectivity needs at least $k + 1$ vertices, since the minimum degree is at least $k$.

**Testing.** Whether $\lambda(G) \ge k$ for a fixed $k$ is decided by computing the [edge connectivity](/edge-connectivity/), or by $n - 1$ maximum flow computations from one vertex, each stopped after $k$ augmenting paths. For $k = 1$ and $k = 2$ one [depth-first search](/depth-first-search/) is enough. The [Nagamochi-Ibaraki certificate](/nagamochi-ibaraki-certificate/) keeps the $k$-edge-connectivity of $G$ with at most $k(n - 1)$ edges, so a test can run on a sparse graph.

## Examples and non-examples

| graph | $\lambda$ | so it is $k$-edge-connected for |
|---|---|---|
| a tree with $n \ge 2$ vertices | 1 | $k \le 1$ |
| a cycle $C_n$, $n \ge 3$ | 2 | $k \le 2$ |
| the [complete graph](/complete-graph/) $K_n$, $n \ge 2$ | $n - 1$ | $k \le n - 1$ |
| the hypercube $Q_d$, $d \ge 1$ | $d$ | $k \le d$ |
| the Petersen graph | 3 | $k \le 3$ |
| two vertices with $k$ parallel edges | $k$ | up to $k$ |
| two triangles sharing a vertex | 2 | $k \le 2$ |
| two copies of $K_4$ joined by two edges at different vertices | 2 | $k \le 2$ |

In the last row each $K_4$ is 3-edge-connected, but the two joining edges form a cut of size 2, so the graph is 2-edge-connected and not 3-edge-connected, although its minimum degree is 3.

Non-examples:

- A single vertex is not $k$-edge-connected for any $k$, by the condition $n \ge 2$. (Some texts make $K_1$ $k$-edge-connected for every $k$; with that wording, $\lambda(K_1)$ is not defined or is $\infty$.)
- A disconnected graph is not $k$-edge-connected for any $k \ge 1$.
- A graph with a loop at every vertex but no other edge is not 1-edge-connected when $n \ge 2$: loops do not help.

## Related definitions

- [Edge connectivity](/edge-connectivity/): the number $\lambda(G)$, and the algorithms that compute it.
- [k-vertex-connected graph](/k-vertex-connected-graph/): the version for vertices, a stronger property.
- [2-edge-connected graph](/two-edge-connected-graph/): the case $k = 2$, and the [2-edge-connected components](/two-edge-connected-components/) of a graph.
- [Menger's theorem](/menger-theorem/): the equivalence with edge-disjoint paths.
- [Strong orientation](/strong-orientation/): a graph has one if and only if it is 2-edge-connected (Robbins). Nash-Williams extended this to $2k$-edge-connected graphs and $k$-arc-strong orientations.
- [Cut](/cut/): the sets $\delta(S)$, whose minimum size is $\lambda(G)$.

## References
