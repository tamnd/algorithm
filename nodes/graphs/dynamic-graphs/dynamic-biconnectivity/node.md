---
tag: FB4NM4
kind: problem
slug: dynamic-biconnectivity
name: Dynamic biconnectivity
aliases:
- dynamic 2-edge connectivity
- dynamic 2-vertex connectivity
area: graphs/dynamic-graphs
level: advanced
summary: Maintain bridges, articulation points or biconnected components under updates.
prereqs: [dynamic-connectivity, bridge, articulation-point, biconnected-components]
see_also: [two-edge-connected-components, online-bridge-finding, holm-de-lichtenberg-thorup, bridge-finding, articulation-point-finding, block-cut-tree, sparsification]
sources:
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: the sections on 2-edge connectivity and biconnectivity (O(log^4 n) and O(log^5 n) amortized per update)
  - paper: doi:10.1137/S0097539792226825
    title: Greg N. Frederickson, Ambivalent data structures for dynamic 2-edge-connectivity and k smallest spanning trees, SIAM Journal on Computing 26(2), 484 to 538 (1997)
    locator: the main results for 2-edge connectivity (O(m^(1/2)) worst-case time per update)
  - paper: doi:10.1007/BF01758773
    title: Jeffery Westbrook and Robert E. Tarjan, Maintaining bridge-connected and biconnected components on-line, Algorithmica 7, 433 to 464 (1992)
    locator: the whole paper (the incremental case)
  - paper: doi:10.1137/1.9781611975031.3
    title: Jacob Holm, Eva Rotenberg and Mikkel Thorup, Dynamic bridge-finding in Õ(log^2 n) amortized time, Proceedings of SODA 2018, 35 to 52
    locator: the main theorem
---

Dynamic biconnectivity is the family of problems that keep the two kinds of 2-connectivity of an undirected [dynamic graph](/dynamic-graph/) under edge updates: the [bridges](/bridge/) and [2-edge-connected components](/two-edge-connected-components/), and the [articulation points](/articulation-point/) and [biconnected components](/biconnected-components/). A query asks whether two vertices are joined by two edge-disjoint paths, or by two internally vertex-disjoint paths, or whether an edge is a bridge. These problems extend [dynamic connectivity](/dynamic-connectivity/), and the best fully dynamic algorithms use the same idea of edge levels with a few more logarithmic factors.

## In plain words

A network is fragile at a link if cutting that one link splits it, and fragile at a node if removing that one node splits it. The program must keep track of these weak spots while links are added and removed.

Adding a link can only remove weak spots: the new link gives a second route around the old weak links on the way between its ends. Removing a link can create weak spots far away from it, because some other route may have depended on it. A good structure keeps a skeleton tree of the network and, for each tree link, a count of how many extra links run around it. A tree link with no extra link around it is a weak link.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices, at first with no edges, and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates and queries.

**Queries.** For the current graph:

- $\mathrm{2edge}(u, v)$: true if and only if $G$ has two edge-disjoint paths from $u$ to $v$, which is the same as: $u$ and $v$ are connected and no bridge separates them (by [Menger's theorem](/menger-theorem/)).
- $\mathrm{isbridge}(e)$: true if and only if deleting $e$ increases the number of components.
- $\mathrm{biconn}(u, v)$ for $u \ne v$: true if and only if $u$ and $v$ lie on a common simple cycle, or are joined by an edge; equivalently some biconnected component contains both.
- $\mathrm{isarticulation}(x)$: true if and only if deleting $x$ increases the number of components.

**Output.** The answer to each query before the next operation is read.

The **2-edge** problem asks for the first two queries, and the **biconnectivity** (2-vertex) problem for the last two. Updates are insertions only (incremental), deletions only (decremental), or both (fully dynamic). Each bound is worst case, [amortized](/amortized-update-time/) or expected.

## Variants

- **Incremental.** Insertions only. An insertion between two vertices of one component merges all 2-edge-connected components on the tree path between them into one, and a [disjoint-set](/disjoint-set/) structure keeps these merges; see [online bridge finding](/online-bridge-finding/). Westbrook and Tarjan (1992) solve both the bridge and the biconnected versions in nearly linear total time.
- **Decremental.** Deletions only.
- **Fully dynamic.** Both.
- **Counting.** Keep the number of bridges, or of articulation points.
- **Higher connectivity.** Keep 3-edge-connected or 3-vertex-connected components, or decide $k$-edge connectivity for a fixed $k$; see [edge connectivity](/edge-connectivity/).
- **Dynamic forests with cover counts.** On a [dynamic tree](/dynamic-tree/) with extra non-tree edges, an edge of the tree is a bridge exactly when no non-tree edge covers it; [top trees](/top-tree/) keep these cover counts.

## Examples

Take $V = \{0, \ldots, 5\}$ and start from the edges $01, 12, 20, 23, 34, 45$: a triangle $0, 1, 2$ with a path $2, 3, 4, 5$ hanging from it. The table gives the bridges and the articulation points after each update.

| update | bridges | articulation points |
|---|---|---|
| start | 23, 34, 45 | 2, 3, 4 |
| insert(5, 3) | 23 | 2, 3 |
| insert(0, 4) | none | none |
| delete(2, 0) | none | none |
| delete(3, 4) | none | none |
| delete(0, 1) | 04, 12, 23, 45, 53 | 2, 3, 4, 5 |

Inserting $53$ closes the cycle $3, 4, 5$, so $34$ and $45$ stop being bridges at once. Inserting $04$ closes a cycle through the triangle and the path, so the graph becomes 2-vertex-connected. The two deletions that follow leave the 6-cycle $0, 1, 2, 3, 5, 4$, which has no weak spot. The last deletion opens that cycle into a path, and every edge of the path becomes a bridge. One deletion created five bridges, which shows why deletions are the hard updates.

**2-edge but not biconnected.** Two triangles that share one vertex $x$ have no bridge, so all vertices are pairwise 2-edge-connected. But $x$ is an articulation point, so two vertices from different triangles are not biconnected.

## Known algorithms

**Static.** One [depth-first search](/depth-first-search/) with [low-link](/low-link/) values finds all bridges and articulation points in $O(n + m)$ time; see [bridge finding](/bridge-finding/) and [articulation point finding](/articulation-point-finding/). Recomputing after each update costs $O(n + m)$ per update.

**Fully dynamic.**

| algorithm | problem | update time | case | deterministic |
|---|---|---|---|---|
| Frederickson (1997), ambivalent data structures | 2-edge | $O(m^{1/2})$ | worst | yes |
| [sparsification](/sparsification/) over it | 2-edge | $O(n^{1/2})$ | worst | yes |
| [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/) (2001) | 2-edge | $O(\log^4 n)$ | amortized | yes |
| Holm, de Lichtenberg and Thorup (2001) | biconnectivity | $O(\log^5 n)$ | amortized | yes |
| Holm, Rotenberg and Thorup (2018) | 2-edge | $\tilde O(\log^2 n)$ | amortized | yes |

The polylogarithmic algorithms keep a spanning forest $F$ in a [top tree](/top-tree/) or an equivalent structure. Each non-tree edge $\{u, v\}$ *covers* the tree path from $u$ to $v$. A tree edge is a bridge exactly when no non-tree edge covers it, because a covering edge closes a cycle through it, and a cycle through it exists only if some non-tree edge's fundamental cycle passes through it. Inserting a non-tree edge raises the cover counts on its path, and deleting one lowers them. Deleting a tree edge needs a replacement tree edge, as in dynamic connectivity, and the replacement changes the paths that the other non-tree edges cover. The edge levels bound this work in the amortized sense.

## Bounds

**Upper bounds.** As in the table; with polylogarithmic queries, the 2-edge problem is solved in $\tilde O(\log^2 n)$ amortized time per update and the biconnectivity problem in $O(\log^5 n)$, both deterministic.

**Lower bounds.** Dynamic connectivity reduces to both problems (see below), so the $\Omega(\log n)$ cell-probe bound of the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/) also holds for them, for the larger of the update and the query time.

## Reductions

- **From connectivity to 2-edge connectivity.** Replace each edge $\{u, v\}$ of a connectivity instance by two parallel edges, or, if the structure does not accept multigraphs, by the two paths $u, a, v$ and $u, b, v$ through two new vertices. Then two vertices are 2-edge-connected exactly when they were connected. So 2-edge connectivity is at least as hard as connectivity, up to a constant factor in the size.
- **From connectivity to biconnectivity.** At the start, add a new vertex $z$ with an edge to every vertex, and then run the connectivity updates unchanged. If $u \ne v$ are connected in $G$, a path from $u$ to $v$ in $G$ and the path $u, z, v$ are internally disjoint, so $u$ and $v$ are biconnected. If they are not connected in $G$, every path between them passes through $z$, so they are not. Each query of connectivity becomes one query of biconnectivity.
- **Block-cut tree.** A static [block-cut tree](/block-cut-tree/) turns biconnectivity queries into tree queries; a dynamic version of this tree is the core of the vertex version.

## Applications

- **Network reliability.** Report the links and routers whose failure alone would disconnect a network, as the network changes.
- **Planarity and embedding.** Algorithms for [dynamic planarity testing](/dynamic-planarity-testing/) work on biconnected and triconnected components, so they need these structures as parts.
- **Edge-disjoint routing.** A 2-edge query tells whether a backup route that shares no link with the main route exists.

## References
