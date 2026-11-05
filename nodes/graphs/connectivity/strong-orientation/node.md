---
tag: 5J950J
kind: problem
slug: strong-orientation
name: Strong orientation
area: graphs/connectivity
level: core
summary: Problem of orienting the edges of an undirected graph so it becomes strongly connected, possible exactly when the graph is bridgeless and connected.
prereqs: [two-edge-connected-graph, strongly-connected-graph, depth-first-search, low-link]
see_also: [two-edge-connected-components, bridge, bridge-finding, strongly-connected-components, ear-decomposition, edge-classification, menger-theorem, k-edge-connected-graph]
sources:
  - paper: doi:10.2307/2303897
    title: H. E. Robbins, A theorem on graphs, with an application to a problem of traffic control, American Mathematical Monthly 46(5), 281 to 283 (1939)
    locator: the whole paper (a graph has a strongly connected orientation exactly when it is connected and has no bridge)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the sections on depth-first search of undirected graphs and the low point
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.2, k-connected graphs (Robbins' theorem by closed-ear decompositions)
  - paper: doi:10.4153/CJM-1960-049-6
    title: C. St. J. A. Nash-Williams, On orientations, connectivity and odd-vertex-pairings in finite graphs, Canadian Journal of Mathematics 12, 555 to 567 (1960)
    locator: the orientation theorem (a graph has a k-arc-connected orientation exactly when it is 2k-edge-connected)
  - paper: doi:10.1080/00029890.1980.11995131
    title: F. Boesch and R. Tindell, Robbins's theorem for mixed multigraphs, American Mathematical Monthly 87(9), 716 to 719 (1980)
    locator: the whole paper (the version where some edges are already directed)
  - paper: doi:10.1016/0095-8956(78)90078-3
    title: V. Chvátal and C. Thomassen, Distances in orientations of graphs, Journal of Combinatorial Theory, Series B 24(1), 61 to 75 (1978)
    locator: the whole paper (bounds on the radius and diameter of strong orientations, and the NP-hardness of deciding oriented diameter 2)
---

The strong orientation problem asks for a direction on each edge of an undirected graph such that the resulting [directed graph](/directed-graph/) is [strongly connected](/strongly-connected-graph/). Robbins proved in 1939 that such a direction exists exactly when the graph is connected and has no [bridge](/bridge/), that is, when it is [2-edge-connected](/two-edge-connected-graph/). One [depth-first search](/depth-first-search/) both decides the question and builds the orientation, in $\Theta(n + m)$ time: point tree edges down and all other edges up.

## In plain words

A town wants to make every street one-way, and still let every driver get from any place to any other place. When can it do that?

If some street is the only link between two parts of the town, it cannot: whichever way that street points, one part can no longer reach the other. Robbins showed that this is the only obstacle. If every street lies on some loop, a good choice always exists.

A depth-first walk through the town finds one. Each time the walk enters a new street towards an unvisited place, make the street point the way the walk went. Every other street leads back to a place visited earlier on the current route; make it point back there. Every place can then be reached from the start, and the back streets lead from every place back to the start.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. [Parallel edges](/multigraph/) and [self-loops](/self-loop/) are allowed; parallel copies may get different directions, and a loop is a loop either way.

**Orientation.** An *orientation* of $G$ replaces each edge $\{u, v\}$ by one of the arcs $(u, v)$ or $(v, u)$. It is *strong* if the resulting directed graph $D$ is strongly connected.

**Output.** A strong orientation of $G$, or the answer that none exists. The decision version asks only whether one exists.

**Theorem (Robbins).** $G$ has a strong orientation if and only if it is connected and has no bridge.

*Proof.* If $D$ is strongly connected, $G$ is connected. If $e = \{u, v\}$, $u \ne v$, is oriented as $(u, v)$, then $D$ has a directed path from $v$ to $u$, which does not use $e$, so $G - e$ still joins $u$ and $v$, and $e$ is not a bridge.

Conversely, let $G$ be connected and bridgeless. Run a depth-first search from a vertex $r$ that treats edges by identity, so that it skips only the one edge by which it entered a vertex. Every edge is a tree edge or a non-tree edge, and every non-tree edge joins a vertex to one of its ancestors (see [edge classification](/edge-classification/)). Orient each tree edge from parent to child, and each non-tree edge from the descendant to the ancestor. Let $d$ be the preorder numbers and $\mathrm{low}$ the [low points](/low-link/).

Every vertex is reachable from $r$ along tree arcs. We show by induction on the depth that every vertex $c$ reaches $r$. The root does. Let $c \ne r$ have parent $p$. The tree edge $\{p, c\}$ is not a bridge, so by the bridge criterion $\mathrm{low}[c] \le d[p] < d[c]$. So some vertex $x$ in the subtree of $c$ has a non-tree edge to an ancestor $w$ of $x$ with $d[w] = \mathrm{low}[c] < d[c]$. As $w$ is an ancestor of $x$ and not in the subtree of $c$, it is a proper ancestor of $c$, of smaller depth. In $D$, $c$ reaches $x$ along tree arcs and then $w$ by the arc $(x, w)$, and $w$ reaches $r$ by induction. So $D$ is strongly connected. $\square$

## Variants

- **Mixed graphs.** Some edges are already directed and only the others may be oriented. Boesch and Tindell extended Robbins' theorem to this case: a strong orientation exists exactly when the mixed graph is strongly connected, with undirected edges usable both ways, and no undirected edge is a bridge of the underlying undirected graph.
- **Higher connectivity.** Nash-Williams proved that a graph has an orientation in which every two vertices are joined by $k$ arc-disjoint directed paths exactly when it is $2k$-edge-connected. Robbins' theorem is the case $k = 1$.
- **Small diameter.** Among the strong orientations, find one whose directed distances are small. Chvátal and Thomassen proved that every bridgeless graph of radius $\rho$ has a strong orientation of radius at most $\rho^2 + \rho$, and that deciding whether a graph has a strong orientation of diameter 2 is NP-hard.
- **General graphs.** If $G$ has bridges, orient each [2-edge-connected component](/two-edge-connected-components/) strongly; the bridges cannot be oriented to help. The DFS orientation does this automatically, as shown under Reductions.

## Examples

**Two triangles at a vertex.** Take the edges $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{1,3\}$, $\{3,4\}$, $\{4,1\}$ with the lists in this order. DFS from 0 visits $0, 1, 2$ and then $3, 4$; the tree edges are $\{0,1\}$, $\{1,2\}$, $\{1,3\}$, $\{3,4\}$, and the non-tree edges are $\{2,0\}$ and $\{4,1\}$. The orientation is $0 \to 1 \to 2 \to 0$ and $1 \to 3 \to 4 \to 1$: two directed triangles sharing vertex 1, which is strongly connected although 1 is an [articulation point](/articulation-point/).

**A double edge.** Two vertices joined by two parallel edges: one becomes the tree arc $u \to v$, the other the back arc $v \to u$. With only one edge, the edge is a bridge, and no orientation works.

**A bridge.** Add to the triangles above the edges $\{4, 5\}$, two parallel edges $\{5, 6\}$ and a loop at 6. The edge $\{4, 5\}$ is a bridge, so no strong orientation exists. The DFS orientation gives $4 \to 5$, $5 \to 6$, $6 \to 5$ and the loop; its [strongly connected components](/strongly-connected-components/) are $\{0, 1, 2, 3, 4\}$ and $\{5, 6\}$, the 2-edge-connected components.

**Tree.** A tree with at least 2 vertices has only bridges. Any orientation of a path $a - b - c$ leaves a vertex that cannot reach some other.

## Known algorithms

| Algorithm | Time | Notes |
|---|---|---|
| DFS orientation | $\Theta(n + m)$ | Decides and constructs in one search |
| Ear decomposition (Robbins' proof) | $\Theta(n + m)$ with a linear ear decomposition | Orient the first cycle cyclically and each ear as a directed path |
| Orient, then test | $\Theta(n + m)$ | Any orientation method, followed by a strong connectivity test |

**DFS orientation.** Run the search of the proof and orient as it goes: an edge gets its direction the first time it is scanned. The search scans the edge from the vertex it is at, so the arc points from the current vertex to the other end. For a tree edge that is the child; for a non-tree edge seen first from the descendant that is the ancestor; and a non-tree edge to an ancestor is always seen first from the descendant, because the descendant is the one active when it is scanned. The same search computes $\mathrm{low}$, and $G$ has a strong orientation exactly when the search reaches all vertices and $\mathrm{low}[c] \le d[p]$ for each tree edge $(p, c)$. Without the test, the result can be checked by two searches, one in $D$ and one in its [transpose](/graph-transpose/), from $r$.

**Ears.** A 2-edge-connected graph is one cycle with *ears* added: paths between two vertices already present, or cycles through one. Orient the first cycle cyclically and each ear as a directed path in either direction; each step keeps the graph strongly connected, as the new vertices lie on a directed path from and back to the old part.

## Bounds

- **Time.** $\Theta(n + m)$ is optimal on adjacency lists: an algorithm that does not look at some edge cannot orient it, and in the decision version an unread entry may be a parallel copy of the only bridge.

## Reductions

- **To 2-edge-connected components.** A strong orientation exists exactly when $G$ is connected and has one [2-edge-connected component](/two-edge-connected-components/).
- **DFS orientation computes the components.** For any undirected $G$, the strongly connected components of the DFS orientation are exactly the 2-edge-connected components of $G$, and the bridges are the arcs between components. *Proof.* For a tree edge $\{p, c\}$ that is not a bridge, the proof of Robbins' theorem shows that $c$ reaches a proper ancestor $w$ of $c$, and $w$ reaches $p$ and then $c$ along tree arcs, so $p$ and $c$ are in one component. A non-tree arc $(x, w)$ lies on the cycle formed with the tree path from $w$ to $x$. So the ends of every non-bridge edge lie in one strong component. Conversely, if $u$ and $v$ were in one strong component but different 2-edge-connected components, a bridge $b$ would separate them in $G$, and the directed paths from $u$ to $v$ and from $v$ to $u$ would both cross $b$, in opposite directions, which is impossible for one arc. $\square$
- **To bridge finding.** As above, $G$ has a strong orientation exactly when [bridge finding](/bridge-finding/) reports no bridge and $G$ is connected.

## Applications

- **One-way streets.** Robbins' motivation: a town can make all streets one-way while keeping every place reachable exactly when no street is a bridge. Small-diameter orientations keep the detours short.
- **Networks with one-way links.** In communication networks where links are cheaper or faster in one direction, a strong orientation gives a design in which every node can still reach every other.
- **Proof tool.** The DFS orientation is a quick way to turn undirected 2-edge-connectivity questions into directed strong connectivity questions, as in the reduction above.

## References
