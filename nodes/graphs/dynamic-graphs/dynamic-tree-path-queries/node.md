---
tag: FSCN5C
kind: problem
slug: dynamic-tree-path-queries
name: Dynamic tree path queries
aliases:
- path aggregate queries on dynamic forests
area: graphs/dynamic-graphs
level: advanced
summary: Answer path aggregate queries on a forest while links and cuts occur.
prereqs: [dynamic-tree, tree, monoid]
see_also: [link-cut-tree, top-tree, heavy-light-decomposition, euler-tour-tree, lowest-common-ancestor, segment-tree, dynamic-minimum-spanning-tree, rake-compress-tree]
sources:
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3), 362 to 391 (1983)
    locator: the path operations (minimum cost on a path, add a cost to a path), the heavy and light edges, and the application to maximum flow (O(mn log n) time)
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 652 to 686 (1985)
    locator: the section on link-cut trees implemented with splay trees
  - paper: doi:10.1145/1103963.1103966
    title: Stephen Alstrup, Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Maintaining information in fully dynamic trees with top trees, ACM Transactions on Algorithms 1(2), 243 to 264 (2005)
    locator: the path and non-local queries supported by top trees (O(log n) worst-case time)
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Patrascu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: the abstract and Section 1 (Omega(log n) for partial sums and for connectivity in forests)
---

Dynamic tree path queries is the problem of answering aggregate queries, such as the sum, the minimum or the maximum of values along the path between two vertices, in a forest that changes by `link` and `cut`. It is the path part of the [dynamic tree](/dynamic-tree/) abstract type, and it often comes with path updates that add a value to every vertex or edge on a path. [Link-cut trees](/link-cut-tree/) and [top trees](/top-tree/) solve it in $O(\log n)$ time per operation, which is optimal in the cell-probe model. For a tree that does not change shape, [heavy-light decomposition](/heavy-light-decomposition/) with a [segment tree](/segment-tree/) gives a simpler $O(\log^2 n)$ solution.

## In plain words

A road network has no loops, so there is exactly one route between two towns, if any. Each road has a number, such as its toll or its height limit. People ask about the route between two towns: what is the total toll, or what is the lowest height limit on it? Roads are built and closed over time, but never so that a loop appears.

Walking along the route answers each question, but the route can be very long. A good structure keeps the routes in pieces inside balanced trees, so that each question, each new road and each closed road takes only a number of steps that grows with the logarithm of the number of towns.

## Definition

**Input.** A forest $F$ on $n$ vertices with values $\mathrm{val}(x)$ in a monoid $(M, \oplus)$ on the vertices or on the edges, and an online sequence of operations:

- $\mathrm{link}(u, v)$ for $u, v$ in different trees, and $\mathrm{cut}(u, v)$ for an edge $\{u, v\}$ of $F$,
- $\mathrm{set}(x, a)$, which changes one value,
- $\mathrm{path\text{-}update}(u, v, \delta)$, which applies $\delta$ to every value on the path from $u$ to $v$,
- $\mathrm{query}(u, v)$, which returns $\bigoplus$ of the values on the path from $u$ to $v$, in path order, or reports that $u$ and $v$ are in different trees.

**Output.** The answer to each query before the next operation is read.

**Requirements on the values.** The structure stores aggregates of subpaths, so $\oplus$ must be associative. If $\oplus$ is not commutative, the structure also stores the aggregate in the reverse order, for the case that it must reverse a path. A path update must act on aggregates: from the aggregate of a subpath and its length, the structure must compute the aggregate after the update. Adding a constant works with $\min$, $\max$ and $+$.

## Variants

- **Path minimum or maximum.** The most common case. Path maximum over edge weights decides whether an edge belongs in a minimum spanning tree.
- **Path sum and path length.** The distance between two vertices in a weighted tree.
- **Path update.** Add a value to all edges on a path, as in augmenting a flow along a path.
- **Rooted queries.** The path from a vertex to the root of its tree, as in the original Sleator-Tarjan interface, or the lowest common ancestor of two vertices in a rooted forest.
- **Static shape.** The tree never changes, and only values change; see [heavy-light decomposition](/heavy-light-decomposition/).
- **Subtree queries.** Aggregates over a subtree instead of a path; these suit [Euler tour trees](/euler-tour-tree/).

## Examples

Take vertices $0, \ldots, 6$ and the tree with edges $01$ (7), $12$ (3), $13$ (9), $34$ (2), $45$ (6), $26$ (5), with weights on the edges.

| operation | path | max | sum |
|---|---|---|---|
| query(0, 5) | 0, 1, 3, 4, 5 | 9 | 24 |
| query(6, 5) | 6, 2, 1, 3, 4, 5 | 9 | 25 |
| query(2, 4) | 2, 1, 3, 4 | 9 | 14 |
| cut(1, 3) | | | |
| query(6, 5) | none, different trees | | |
| link(6, 4) with weight 4 | | | |
| query(0, 5) | 0, 1, 2, 6, 4, 5 | 7 | 25 |
| query(3, 2) | 3, 4, 6, 2 | 5 | 11 |

The cut and the link together are one step of a [dynamic minimum spanning tree](/dynamic-minimum-spanning-tree/). A new edge $\{6, 4\}$ of weight 4 arrives. The path from 6 to 4 in the tree is $6, 2, 1, 3, 4$, and its maximum edge is $13$ with weight 9. Since $4 < 9$, the tree swaps $13$ for $64$, which lowers its total weight by 5.

## Known algorithms

| method | link, cut | query, path update | case | deterministic |
|---|---|---|---|---|
| walk the path with parent pointers | $O(1)$ | $O(n)$ | worst | yes |
| [heavy-light decomposition](/heavy-light-decomposition/) with a [segment tree](/segment-tree/), static shape | not supported | $O(\log^2 n)$ | worst | yes |
| [link-cut tree](/link-cut-tree/) with [splay trees](/splay-tree/) | $O(\log n)$ | $O(\log n)$ | amortized | yes |
| link-cut tree with biased search trees | $O(\log n)$ | $O(\log n)$ | worst | yes |
| [top tree](/top-tree/) | $O(\log n)$ | $O(\log n)$ | worst | yes |
| [rake-compress tree](/rake-compress-tree/) | $O(\log n)$ | $O(\log n)$ | expected | no |

**Link-cut trees.** Each tree is split into vertex-disjoint *preferred paths*, and each preferred path is a search tree keyed by depth whose nodes store the aggregate of their subtree, with a lazy tag for pending path updates. An `access(v)` makes the path from $v$ to the root preferred, and `evert(u)` makes $u$ the root, so a query on $u, v$ is `evert(u)`, `access(v)`, and a read of the aggregate at the root of one search tree. The number of preferred-path changes per access is $O(\log n)$ amortized, by the heavy-light argument of Sleator and Tarjan, and splaying makes the total cost $O(\log n)$ amortized per operation.

**Heavy-light decomposition.** For a fixed tree, an edge from a vertex to its child of largest subtree is *heavy*. Every path from a vertex to the root uses $O(\log n)$ light edges, so it splits into $O(\log n)$ pieces of heavy paths. With the heavy paths laid out in one array under a segment tree, a query costs $O(\log n)$ segments of $O(\log n)$ each. It does not support `link` and `cut`, because these change the heavy paths.

**Top trees.** A top tree is a balanced hierarchy of clusters, each a connected part of the tree with at most two boundary vertices. Each cluster stores the aggregate of the path between its boundary vertices. A link or cut changes $O(\log n)$ clusters, and a path query exposes the two vertices as boundary vertices of the root cluster.

## Bounds

**Upper bound.** $O(\log n)$ per operation, amortized and deterministic with splay-based link-cut trees, worst case with biased link-cut trees or top trees.

**Lower bound.** Pătraşcu and Demaine (2006) prove that the partial sums problem, in which values on a single path change and queries ask for prefix sums, needs $\Omega(\log n)$ time per operation in the [cell-probe model](/cell-probe-model/), for the larger of update and query time, amortized and also for randomized structures. A forest that is a single path, with sums as the aggregate, is a special case of this problem. The same paper proves $\Omega(\log n)$ for connectivity in forests, which a path query also answers. So $O(\log n)$ is optimal, even when the shape never changes.

## Reductions

- **Partial sums to path queries.** As above: a path is a tree.
- **Forest connectivity to path queries.** $u$ and $v$ are connected exactly when the query does not report different trees.
- **Edge values to vertex values.** Subdivide each edge by a new vertex that holds its value, or, in a rooted tree, store each edge value at the lower end of the edge and leave out the top vertex of the path.

## Applications

- **Maximum flow.** Sleator and Tarjan (1983) used path minimum and path update on a forest of residual edges to find blocking flows, which gives maximum flow in $O(mn \log n)$ time.
- **Minimum spanning trees.** Path maximum decides whether a new edge enters a minimum spanning tree, and which edge it replaces, in incremental and [dynamic minimum spanning tree](/dynamic-minimum-spanning-tree/) algorithms.
- **Network simplex.** Each pivot adds an edge to a spanning tree, finds the minimum on the cycle it closes, and removes an edge.
- **Competitive programming.** Path sums and updates on trees, with or without links and cuts, are standard tasks.

## References
