---
tag: TDYP8H
kind: theorem
slug: menger-theorem
name: Menger's theorem
aliases:
- Menger's theorem for vertices and edges
area: graphs/connectivity
level: core
summary: The maximum number of internally disjoint s-t paths equals the minimum s-t vertex cut.
prereqs: [vertex-cut, cut, max-flow-min-cut-theorem, flow-integrality-theorem, flow-decomposition]
see_also: [vertex-connectivity, edge-connectivity, vertex-disjoint-paths, edge-disjoint-paths, vertex-capacities-flow, konig-theorem, k-vertex-connected-graph, k-edge-connected-graph]
sources:
  - paper: doi:10.4064/fm-10-1-96-115
    title: Karl Menger, Zur allgemeinen Kurventheorie, Fundamenta Mathematicae 10(1), 96 to 115 (1927)
    locator: the whole paper (the n-arc theorem, stated for curves and graphs)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.2, k-connected graphs (Menger's theorem in its local and global forms, the edge version, and the proofs by line graphs and by flows)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 3.3, Menger's theorem (the set version, several proofs, and the global forms)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 7.6, Disjoint paths in directed and undirected graphs (the edge version from max-flow min-cut)
---

Menger's theorem says that the number of paths that can run from $s$ to $t$ without sharing anything equals the number of things that must be removed to separate $s$ from $t$. It has a vertex form and an edge form, each for directed and undirected graphs. It is the basic min-max theorem of graph connectivity: it turns the "for every small set, the graph survives" definition of a [$k$-connected graph](/k-vertex-connected-graph/) into the "there are $k$ disjoint routes" form, and it is the special case of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) with unit capacities.

## Statement

Let $G = (V, E)$ be a finite graph, directed or undirected, where [parallel edges](/multigraph/) and [self-loops](/self-loop/) are allowed. Paths are directed paths when $G$ is directed. Two $s$-$t$ paths are *internally disjoint* if they share no vertex other than $s$ and $t$, and *edge-disjoint* if they share no edge; two parallel copies of an edge are different edges. Loops play no role, as no path uses one.

**Theorem (vertex form).** Let $s \ne t$ be vertices such that $G$ has no edge from $s$ to $t$. The largest number of pairwise internally disjoint $s$-$t$ paths equals $\kappa(s, t)$, the least size of an [$s$-$t$ vertex cut](/vertex-cut/), that is, of a set $X \subseteq V \setminus \{s, t\}$ such that $G - X$ has no $s$-$t$ path.

**Theorem (edge form).** Let $s \ne t$ be vertices. The largest number of pairwise edge-disjoint $s$-$t$ paths equals $\lambda(s, t)$, the least size of a set $F \subseteq E$ such that $G - F$ has no $s$-$t$ path.

## In plain words

Pick two places in a road network. Count how many routes you can drive from the first to the second so that no two routes pass through the same crossing on the way. Then count how few crossings you would have to close to cut the first place off from the second. The theorem says the two counts are always equal.

One way is easy: every route must pass through one of the closed crossings, and different routes use different crossings, so there can be no more routes than closed crossings. The hard part is that there is always a set of closed crossings that small: if no small set cuts the two places apart, then many separate routes really exist. The same holds when roads, not crossings, are closed and routes may not share a road.

## Proof

**The easy inequality.** In the vertex form, let $P_1, \ldots, P_k$ be internally disjoint $s$-$t$ paths and $X$ an $s$-$t$ vertex cut. Each $P_i$ is an $s$-$t$ path of $G$, so it meets $X$, at an inner vertex because $s, t \notin X$. The inner vertices of different paths are different, so $|X| \ge k$. The edge form is the same with edges. So the largest number of paths is at most the least size of a cut, in each form. It remains to find, in each form, a family of paths and a cut of the same size.

We use three facts about flows in a network with integer capacities $c$, source $s$ and sink $t$. The [max-flow min-cut theorem](/max-flow-min-cut-theorem/): the largest value of a flow equals the least capacity $c(S, \bar S)$ of a cut, over the sets $S$ with $s \in S$, $t \notin S$, where $\bar S = V \setminus S$ and $c(S, \bar S)$ is the total capacity of the arcs from $S$ to $\bar S$. The [integrality theorem](/flow-integrality-theorem/): some maximum flow has integer values. [Flow decomposition](/flow-decomposition/): a flow of value $F$ with integer values is a sum of $F$ flows of value 1 along $s$-$t$ paths and of flows along cycles, each path or cycle carrying 1 unit, and each arc $a$ lying on at most $f(a)$ of them.

**Directed edge form.** Remove the loops. Give every arc capacity 1, with parallel arcs as separate arcs. Take an integer maximum flow $f$ of value $F$. Its values are 0 or 1, so by flow decomposition it gives $F$ $s$-$t$ paths, and an arc with $f(a) = 1$ lies on at most one of them: the paths are arc-disjoint. Take a minimum cut $(S, \bar S)$; its capacity is $F$, so exactly $F$ arcs go from $S$ to $\bar S$. Every $s$-$t$ path starts in $S$ and ends in $\bar S$, so it uses one of these arcs. Their set is a set of $F$ arcs that meets every $s$-$t$ path, so $\lambda(s, t) \le F$. With the easy inequality, both numbers equal $F$.

**Undirected edge form.** Replace each edge $\{u, v\}$ by the two arcs $(u, v)$ and $(v, u)$, each of capacity 1, and take an integer maximum flow $f$ of value $F$. If both arcs of an edge carry 1, set both to 0. This keeps the value and the conservation at every vertex, as it removes one unit into and one unit out of each end. Now each edge carries flow in at most one direction, so the $F$ arc-disjoint paths from flow decomposition use different edges, and they are $F$ edge-disjoint paths of $G$. A minimum cut $(S, \bar S)$ has capacity $F$; each edge between $S$ and $\bar S$ gives exactly one arc from $S$ to $\bar S$, so there are exactly $F$ such edges. Every $s$-$t$ path of $G$ uses one of them, so $\lambda(s, t) \le F$.

**Directed vertex form.** Let $s$ and $t$ be non-adjacent, and $n = |V|$. Build a network $N$ by [vertex splitting](/vertex-capacities-flow/): each vertex $v \ne s, t$ becomes two nodes $v^-$ and $v^+$ with an arc $(v^-, v^+)$ of capacity 1, called the *split arc* of $v$. Write $s^+ = s$ and $t^- = t$. Each arc $(u, v)$ of $G$ with $u \ne t$ and $v \ne s$ becomes an arc $(u^+, v^-)$ of capacity $n$. Arcs into $s$ or out of $t$, and loops, are dropped, as no $s$-$t$ path uses them.

The node $v^-$ has one outgoing arc, its split arc, and $v^+$ has one incoming arc. So a path of $N$ from $s$ to $t$ that enters $v^-$ goes on through the split arc to $v^+$, and it is the image of an $s$-$t$ path of $G$ through the same vertices. Conversely each $s$-$t$ path of $G$ gives such a path of $N$.

Take an integer maximum flow of value $F$ in $N$, and decompose it. A path through the vertex $v$ uses the split arc of $v$, which carries at most 1, so at most one of the $F$ paths passes through $v$: their images are $F$ internally disjoint $s$-$t$ paths of $G$.

Now take a minimum cut $(S, \bar S)$ of $N$, of capacity $F$. Let $S_0 = \{s\} \cup \{v^- : v \ne s, t\}$. Each arc leaving $S_0$ is a split arc, because $s$ has no arc to $t$, so $c(S_0, \bar S_0) \le n - 2 < n$. So $F < n$, and the minimum cut contains no arc of capacity $n$: all its arcs are split arcs. Let $X$ be the set of their vertices; then $|X| = F$. Every $s$-$t$ path of $G$ gives a path of $N$ from $S$ to $\bar S$, which uses an arc from $S$ to $\bar S$, so it uses the split arc of a vertex of $X$. So $X$ is an $s$-$t$ vertex cut and $\kappa(s, t) \le F$.

**Undirected vertex form.** Replace each edge $\{u, v\}$ by the arcs $(u, v)$ and $(v, u)$, giving a directed graph $D$. The $s$-$t$ paths of $G$ and of $D$ are the same sequences of vertices. So internally disjoint paths of $D$ are internally disjoint paths of $G$, and a set that meets every $s$-$t$ path of $D$ meets every $s$-$t$ path of $G$. The directed vertex form for $D$ gives the result for $G$. $\blacksquare$

## Consequences

- **Global vertex form (Whitney).** An undirected graph $G$ with at least $k + 1$ vertices is [$k$-vertex-connected](/k-vertex-connected-graph/) if and only if any two distinct vertices are joined by $k$ internally disjoint paths. *Proof.* If such paths exist, removing fewer than $k$ vertices leaves, for any two surviving vertices, one of the $k$ paths whole, so $G$ is $k$-connected. Conversely, let $G$ be $k$-connected and $u \ne v$. If $u$ and $v$ are not adjacent, a $u$-$v$ vertex cut is a vertex cut of $G$, so $\kappa(u, v) \ge k$, and the vertex form gives $k$ paths. If they are adjacent, let $G'$ be $G$ without the edges between $u$ and $v$. Suppose a set $X$ with $|X| \le k - 2$ separates $u$ from $v$ in $G'$. As $n \ge k + 1$, some vertex $w$ is outside $X \cup \{u, v\}$. In $G' - X$, $w$ is not in the part of $u$ or not in the part of $v$; say not in that of $u$. Then $X \cup \{v\}$ has at most $k - 1$ vertices and separates $u$ from $w$ in $G$, as the edges $uv$ are gone with $v$. This contradicts $k$-connectivity. So $\kappa_{G'}(u, v) \ge k - 1$, the vertex form gives $k - 1$ internally disjoint paths in $G'$, and the edge $uv$ is the $k$-th. $\square$
- **Global edge form.** A graph is [$k$-edge-connected](/k-edge-connected-graph/) if and only if any two vertices are joined by $k$ edge-disjoint paths. This is the edge form for every pair.
- **Set form.** For sets $A, B \subseteq V$, the largest number of vertex-disjoint paths from $A$ to $B$ equals the least size of a set of vertices that meets every path from $A$ to $B$. *Proof.* Add a new vertex $s$ joined to all of $A$ and a new vertex $t$ joined from all of $B$, and apply the vertex form to $s$ and $t$. $\square$
- **Kőnig's theorem.** In a bipartite graph with sides $A$ and $B$, a family of disjoint $A$-$B$ paths with no inner vertex in $A \cup B$ is a matching, and a set meeting every $A$-$B$ edge is a vertex cover. So the set form gives [Kőnig's theorem](/konig-theorem/): the largest matching has the size of the least [vertex cover](/vertex-cover/).
- **Algorithms.** The proof is a computation: $\kappa(s, t)$ and $\lambda(s, t)$ are maximum flows in unit-capacity networks, which [Dinic's algorithm](/dinic/) solves in $O(m \sqrt n)$ time for the vertex form and $O(m \min(m^{1/2}, n^{2/3}))$ time for the edge form. The minimum cut of the flow gives the cut, and the decomposition gives the paths. These are the building blocks of [vertex connectivity](/vertex-connectivity/) and [edge connectivity](/edge-connectivity/) algorithms.
- **2-connected graphs.** For $k = 2$: a graph with at least 3 vertices is [biconnected](/biconnected-graph/) if and only if any two vertices lie on a common cycle.

## Tightness

- **Adjacent ends.** The vertex form needs $s$ and $t$ non-adjacent. In $K_n$, any two vertices are joined by $n - 1$ internally disjoint paths (the edge and $n - 2$ paths of length 2), but no vertex cut exists.
- **Vertex and edge numbers differ.** Take two triangles $\{s, a, c\}$ and $\{c, b, t\}$ that share the vertex $c$. Then $\lambda(s, t) = 2$, by the edge-disjoint paths $s - c - t$ and $s - a - c - b - t$, but $\kappa(s, t) = 1$, as $\{c\}$ separates. So the two forms are different theorems. In general only $\kappa(s, t) \le \lambda(s, t)$ holds, for non-adjacent $s$ and $t$: each edge of a cut has an end other than $s$ and $t$, and these ends form a vertex cut.
- **Different pairs.** No such min-max holds for paths joining different pairs $s_1$-$t_1$ and $s_2$-$t_2$. In the 4-cycle $s_1, s_2, t_1, t_2$, in this order, no non-terminal vertex exists to separate anything, yet the two pairs cannot be joined by disjoint paths. This is the [disjoint paths](/parameterized-disjoint-paths/) problem, which is NP-complete when the number of pairs is part of the input.
- **Directions matter.** In a directed graph, the paths from $s$ to $t$ and those from $t$ to $s$ are separate questions. With the arcs $s \to a \to t$, $s \to b \to t$ and $t \to c \to s$, $\kappa(s, t) = 2$ but $\kappa(t, s) = 1$.

## History

Karl Menger published the theorem in 1927, in a paper on the theory of curves. Hassler Whitney gave the global form for $k$-connected graphs in 1932. Ford and Fulkerson's max-flow min-cut theorem of 1956 put it in the frame of network flows, which gives the proof above and a polynomial algorithm.

## References
