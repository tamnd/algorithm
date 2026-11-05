---
tag: 5SJ1CE
kind: abstract-type
slug: dynamic-tree
name: Dynamic tree
aliases:
- dynamic forest
- dynamic tree data type
area: graphs/dynamic-graphs
level: advanced
summary: A forest maintained under link and cut operations that answers path and subtree queries.
prereqs: [dynamic-graph, tree, rooted-tree, binary-search-tree]
see_also: [link-cut-tree, euler-tour-tree, top-tree, rake-compress-tree, frederickson-topology-trees, splay-tree, dynamic-tree-path-queries, dynamic-connectivity]
sources:
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3), 362 to 391 (1983)
    locator: Section 1 (the operations on a forest of rooted trees) and the main theorem (O(log n) time per operation)
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 652 to 686 (1985)
    locator: the section on link-cut trees implemented with splay trees (O(log n) amortized per operation)
  - paper: doi:10.1145/1103963.1103966
    title: Stephen Alstrup, Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Maintaining information in fully dynamic trees with top trees, ACM Transactions on Algorithms 1(2), 243 to 264 (2005)
    locator: Section 1 (the interface of top trees, and the comparison with other dynamic tree structures) and the main theorem (O(log n) worst-case time)
  - paper: doi:10.1007/BF02614369
    title: Robert E. Tarjan, Dynamic trees as search trees via Euler tours, applied to the network simplex algorithm, Mathematical Programming 78(2), 169 to 177 (1997)
    locator: the whole paper (Euler tour trees with link, cut and subtree operations)
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Patrascu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: the abstract and Section 1 (Omega(log n) per operation for connectivity in forests)
---

A dynamic tree is an abstract data type that holds a forest on a fixed set of vertices, with values on the vertices or edges, and supports `link`, which joins two trees by a new edge, `cut`, which removes an edge, and queries about the path between two vertices or about a subtree. It is the special case of a [dynamic graph](/dynamic-graph/) in which the graph never has a cycle. The main implementations, the [link-cut tree](/link-cut-tree/), the [Euler tour tree](/euler-tour-tree/), the [top tree](/top-tree/) and the [rake-compress tree](/rake-compress-tree/), all do each operation in $O(\log n)$ time, and this is optimal in the cell-probe model.

## In plain words

Think of a set of ropes that join posts. No loop of ropes is allowed. You can tie a new rope between two posts that are not yet joined, or untie a rope. Each post has a number on it, for example how much weight it can hold.

You want to ask questions such as: are these two posts joined, through any number of ropes? On the way from this post to that one, which post is the weakest? What is the total over all posts on that way? You may also want to raise all the numbers on one way at once.

Walking along the ropes answers each question, but a way can pass through almost every post. A dynamic tree stores the forest in balanced search trees, so that each tie, untie and question takes time that grows only with the logarithm of the number of posts.

## Operations

Let $F$ be a forest on a vertex set $V$ with $|V| = n$, and let each vertex $v$ carry a value $\mathrm{val}(v)$ from a monoid $(M, \oplus)$, for example numbers with $\min$ or with $+$. For two vertices $u, v$ in one tree, $\mathrm{path}_F(u, v)$ is the unique simple path from $u$ to $v$ in $F$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}(V, \mathrm{val}) \to F$ | the forest on $V$ with no edges |
| `link` | $\text{link}(F, u, v) \to F$ | for $u, v$ in different trees: adds the edge $\{u, v\}$ |
| `cut` | $\text{cut}(F, u, v) \to F$ | for an edge $\{u, v\}$ of $F$: removes it |
| `connected` | $\text{connected}(F, u, v) \to \text{bool}$ | whether $u$ and $v$ are in one tree |
| `path-aggregate` | $\text{path-aggregate}(F, u, v) \to M$ | for connected $u, v$: $\bigoplus_{x \in \mathrm{path}_F(u, v)} \mathrm{val}(x)$, in path order |
| `set` | $\text{set}(F, v, a) \to F$ | sets $\mathrm{val}(v) = a$ |
| `path-update` | $\text{path-update}(F, u, v, \delta) \to F$ | applies $\delta$ to the value of every vertex on $\mathrm{path}_F(u, v)$ |

**Rooted operations.** Sleator and Tarjan (1983) state the type for a forest of rooted trees. There `link(v, w)` makes the root $v$ a child of $w$, `cut(v)` removes the edge from $v$ to its parent, `find-root(v)` returns the root of the tree of $v$, and `evert(v)`, also called `make-root`, makes $v$ the root of its tree. With `evert`, the rooted and the unrooted forms give each other in $O(1)$ extra operations. Other common queries are `lca(u, v)` for a rooted tree, `subtree-aggregate(v)` over the subtree of $v$, and the size of a tree.

**Edge values.** Values on edges reduce to values on vertices: subdivide each edge $\{u, v\}$ by a new vertex $e$ that holds the edge value, so `link(u, v)` becomes `link(u, e)` and `link(e, v)`.

The type has no operation that adds an edge inside one tree. That operation would close a cycle, and graphs with cycles need structures such as those for [dynamic connectivity](/dynamic-connectivity/), which often keep a spanning forest in a dynamic tree.

## Laws

For all forests $F$, all vertices $x, y, u, v$, and $\mathrm{conn} = \text{connected}$:

$$\begin{aligned}
&(\text{T1})\quad \mathrm{conn}(\text{link}(F, u, v), x, y) \iff \mathrm{conn}(F, x, y) \text{ or } \big(\mathrm{conn}(F, x, u) \text{ and } \mathrm{conn}(F, v, y)\big) \text{ or } \big(\mathrm{conn}(F, x, v) \text{ and } \mathrm{conn}(F, u, y)\big),\\
&(\text{T2})\quad \text{cut}(\text{link}(F, u, v), u, v) = F \quad \text{if } \neg\, \mathrm{conn}(F, u, v),\\
&(\text{T3})\quad \neg\, \mathrm{conn}(\text{cut}(F, u, v), u, v), \text{ and the cut changes } \mathrm{conn} \text{ only for pairs separated by the edge } \{u, v\},\\
&(\text{T4})\quad \text{path-aggregate}(F, u, v) = \mathrm{val}(x_0) \oplus \mathrm{val}(x_1) \oplus \cdots \oplus \mathrm{val}(x_k) \text{ for } \mathrm{path}_F(u, v) = x_0, \ldots, x_k,\\
&(\text{T5})\quad \text{path-update}(F, u, v, \delta) \text{ changes } \mathrm{val}(x) \text{ exactly for } x \in \mathrm{path}_F(u, v).
\end{aligned}$$

(T1) says that a link merges exactly two trees. (T2) says that a cut undoes a link. (T3) says that a cut splits one tree into the two parts on the sides of the removed edge. (T4) fixes the answer of a path query, including the order of the terms when $\oplus$ is not commutative; then $\text{path-aggregate}(F, v, u)$ is the aggregate in the reverse order. (T5) says that a path update touches nothing outside the path. Queries do not change $F$ or the values, even if an implementation changes its internal shape, as splay-based ones do.

**Example.** Take $V = \{0, \ldots, 5\}$ with values $5, 3, 8, 1, 6, 4$, and $\oplus$ either $\min$ or $+$.

| operation | result |
|---|---|
| link(0, 1), link(1, 2), link(3, 4) | trees $\{0, 1, 2\}$, $\{3, 4\}$, $\{5\}$ |
| connected(0, 4) | false |
| link(2, 3) | trees $\{0, 1, 2, 3, 4\}$, $\{5\}$ |
| path-aggregate(0, 4) with min | 1, on the path 0, 1, 2, 3, 4 |
| path-aggregate(1, 4) with + | 18 |
| link(4, 5), then cut(1, 2) | trees $\{0, 1\}$, $\{2, 3, 4, 5\}$ |
| connected(0, 5) | false |
| path-aggregate(2, 5) with min | 1 |
| path-update(2, 5, +10) | values $5, 3, 18, 11, 16, 14$ |
| path-aggregate(3, 5) with min | 11 |
| path-aggregate(0, 1) with + | 8 |

The update on the path from 2 to 5 changes four values and leaves 0 and 1, which are in another tree, as they were.

## Implementations

The costs are per operation, for a forest on $n$ vertices.

| implementation | link, cut | connected | path aggregate and update | subtree aggregate | case |
|---|---|---|---|---|---|
| parent pointers | $O(1)$ | $O(n)$ | $O(n)$ | $O(n)$ | worst, deterministic |
| [link-cut tree](/link-cut-tree/) with [splay trees](/splay-tree/) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | with extra data, for invertible $\oplus$ | amortized, deterministic |
| link-cut tree with biased search trees (Sleator and Tarjan 1983) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | with extra data | worst, deterministic |
| [Euler tour tree](/euler-tour-tree/) on a balanced search tree | $O(\log n)$ | $O(\log n)$ | no | $O(\log n)$ | worst, deterministic |
| [topology tree](/frederickson-topology-trees/) (Frederickson) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | worst, deterministic, degree at most 3 |
| [top tree](/top-tree/) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | worst, deterministic |
| [rake-compress tree](/rake-compress-tree/) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | expected, randomized |

The **link-cut tree** splits each tree into vertex-disjoint paths and keeps each path in a search tree ordered by depth, so a path query becomes a query on one search tree after the path from the vertex to the root is made preferred. It is the simplest structure for path queries. The **Euler tour tree** keeps the Euler tour of each tree as a sequence in a balanced search tree, so `link` and `cut` become a few splits and joins, and a subtree is a contiguous part of the tour. It does not support path queries. The **topology tree** and the **top tree** build a balanced hierarchy of clusters over each tree, and the **rake-compress tree** builds such a hierarchy by random contraction. These three support path and subtree queries together, and top trees also answer non-local queries such as the center or the median of a tree, through a user-defined combination of clusters.

In practice, splay-based link-cut trees are the common choice for path queries and Euler tour trees for subtree and connectivity queries. Both fit in a few hundred lines. Top trees are more general but have larger constants.

## Lower bounds

**Cell-probe model.** Pătraşcu and Demaine (2006) proved that dynamic connectivity in a forest, even in a forest of disjoint paths, needs $\Omega(\log n)$ amortized time per operation in the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ size, also for randomized structures. More exactly, the larger of the update time and the query time is $\Omega(\log n)$. Since `connected` is part of the type, every implementation obeys this bound, so the $O(\log n)$ structures above are optimal. The same paper gives an $\Omega(\log n)$ bound for partial sums, which is the special case of path aggregates with $+$ on a single path.

**Comparison with union-find.** If `cut` is never used, the forest only grows, and connectivity alone is the [disjoint-set](/disjoint-set/) problem, with $O(\alpha(n))$ amortized time per operation. The logarithmic bound is the price of `cut`.

## References
