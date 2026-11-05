---
tag: 92RHMV
kind: problem
slug: tree-path-queries
name: Path queries on trees
area: graphs/tree-algorithms
level: core
summary: Problem of answering queries about the path between two tree nodes, using techniques such as lowest common ancestor and Euler tours.
prereqs: [rooted-tree, lowest-common-ancestor, monoid]
see_also: [heavy-light-decomposition, lca-binary-lifting, euler-tour-technique, link-cut-tree, tarjan-offline-lca, range-minimum-query, level-ancestor-problem, centroid-decomposition]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 18, Tree queries, Sections 18.1 (Finding ancestors), 18.2 (Subtrees and paths), 18.3 (Lowest common ancestor) and 18.4 (Offline algorithms)
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3), 362 to 391 (1983)
    locator: path aggregates (the minimum cost on a path to the root, and adding a value along a path) on a forest that changes by link and cut, in O(log n) amortized time
  - paper: Bernard Chazelle, Computing on a free tree via complexity-preserving mappings, Algorithmica 2, 337 to 361 (1987)
    locator: static path queries over a semigroup, with a trade-off between preprocessing and query time in terms of the inverse Ackermann function
---

Path queries on trees ask for a summary of the values on the unique path between two vertices $u$ and $v$ of a [tree](/tree/): their sum, their minimum or maximum, the number of edges, the $k$-th vertex, and so on, often while values change. The key fact is that the path splits at the [lowest common ancestor](/lowest-common-ancestor/) $\ell = \mathrm{lca}(u, v)$ into two paths toward the root. With invertible values, prefix sums from the root and one LCA query answer a query in $O(1)$ time; with minimum or maximum, [binary lifting](/lca-binary-lifting/) gives $O(\log n)$; with updates, [heavy-light decomposition](/heavy-light-decomposition/) over a [segment tree](/segment-tree/) gives $O(\log^2 n)$; and on a forest that changes, a [link-cut tree](/link-cut-tree/) gives $O(\log n)$ amortized time.

## In plain words

Towns are joined by roads that form a tree, and each town has a number, such as a toll. A question names two towns and asks about the route between them: the total toll, the highest toll, how many roads it has, or the tenth town on the way. Many such questions come, and the tolls may change between them.

Walking the route for each question is slow on a long tree. The trick is to hang the tree from one town, the root. The route from one town to another goes up to the place where their two ways to the root meet, and then down again. So each question becomes two questions about routes toward the root. Facts about routes toward the root can be stored ahead of time, so a question is answered by a few lookups.

## Definition

**Input.** A tree $T$ with the vertices $0, \ldots, n-1$, given as a list of $n - 1$ edges; it is free, and the algorithms root it at $0$. Each vertex $v$ has a value $a(v)$ from a set $S$ with an associative operation $\oplus$, such as $+$ on numbers or $\min$; the tree is not weighted in any other way. Then a sequence of $q$ operations:

- $\mathrm{query}(u, v)$: return $a(p_0) \oplus a(p_1) \oplus \cdots \oplus a(p_k)$, where $p_0 = u, p_1, \ldots, p_k = v$ is the path from $u$ to $v$;
- $\mathrm{update}(v, x)$, in the dynamic version: set $a(v) \leftarrow x$.

**Edge values.** If the values are on edges, put the value of each edge on its lower end in the rooted tree. A path query then combines the values of the vertices of the path except $\mathrm{lca}(u, v)$.

**The split.** Let $\ell = \mathrm{lca}(u, v)$ in the tree rooted at $0$. The path from $u$ to $v$ is the path from $u$ up to $\ell$, followed by the path from $\ell$ down to $v$, and its length is $d(u) + d(v) - 2d(\ell)$, where $d$ is the depth. Every method below uses this split.

## Variants

- **Invertible values, static.** With a group operation such as $+$ or exclusive or, let $P(v)$ be the combined value from the root to $v$. Then the answer is $P(u) + P(v) - 2P(\ell) + a(\ell)$ for sums, and $P(u) \oplus P(v) \oplus a(\ell)$ for exclusive or.
- **Invertible values, point updates.** Changing $a(v)$ by $x$ changes $P(w)$ by $x$ for every $w$ in the subtree of $v$. In the [Euler tour](/euler-tour-technique/) order that subtree is an interval, so a [Fenwick tree](/fenwick-tree/) with range add and point query keeps $P$ in $O(\log n)$ time per operation.
- **Minimum or maximum, static.** These have no inverse. [Binary lifting](/binary-lifting/) stores the minimum over each jump of $2^j$ steps up, and answers in $O(\log n)$ time after $O(n \log n)$ preprocessing.
- **Any monoid, with updates.** [Heavy-light decomposition](/heavy-light-decomposition/) cuts each path into $O(\log n)$ intervals of a fixed vertex order, and a [segment tree](/segment-tree/) over that order answers each interval.
- **Path updates.** "Add $x$ to every vertex on the path" with sum or minimum queries: heavy-light decomposition with a lazy segment tree, or a link-cut tree.
- **Dynamic forest.** Edges are added and removed between queries. [Link-cut trees](/link-cut-tree/) and [top trees](/top-tree/) answer path queries in $O(\log n)$ amortized time per operation.
- **Structure queries.** The length of the path, the $k$-th vertex on it, or whether a vertex $w$ lies on it. The $k$-th vertex reduces to a [level ancestor](/level-ancestor-problem/) query on $u$ or on $v$; $w$ lies on the path if and only if $\mathrm{lca}(u, w) = w$ or $\mathrm{lca}(v, w) = w$, and $\mathrm{lca}(w, \ell) = \ell$.
- **Offline queries.** When all queries are known first, [Tarjan's offline LCA](/tarjan-offline-lca/) finds all the $\ell$ values in nearly linear time, and [Mo's algorithm](/mo-algorithm/) on the Euler tour handles queries such as the number of distinct values on a path.

## Examples

Take the tree with the edges $01, 02, 13, 14, 25, 46, 47$, rooted at $0$, and the values $a = (5, 3, 8, 1, 4, 2, 7, 6)$ for the vertices $0, \ldots, 7$. The root sums are $P = (5, 8, 13, 9, 12, 15, 19, 18)$.

| query | $\ell$ | path | sum, by $P(u) + P(v) - 2P(\ell) + a(\ell)$ | minimum | maximum | edges |
|---|---|---|---|---|---|---|
| $(6, 5)$ | 0 | $6, 4, 1, 0, 2, 5$ | $19 + 15 - 10 + 5 = 29$ | 2 | 8 | 5 |
| $(3, 7)$ | 1 | $3, 1, 4, 7$ | $9 + 18 - 16 + 3 = 14$ | 1 | 6 | 3 |
| $(4, 4)$ | 4 | $4$ | $12 + 12 - 24 + 4 = 4$ | 4 | 4 | 0 |

After $\mathrm{update}(4, 10)$, the values $P(4), P(6), P(7)$, the subtree of $4$, grow by $6$, and the query $(3, 7)$ gives $20$.

The small cases:

- **Single vertex.** The only query is $(0, 0)$, with answer $a(0)$.
- **Path** $0, 1, \ldots, n-1$. A path query is a range query on the array $a$ over the interval from $\min(u, v)$ to $\max(u, v)$. So path queries include [range minimum queries](/range-minimum-query/) and [range sum queries](/range-sum-query/), and every lower bound for those holds here.
- **Star** with centre $0$. Each path has at most three vertices, $u, 0, v$, so each query takes $O(1)$ time with no preprocessing.

## Known algorithms

| method | values | preprocessing | query | update |
|---|---|---|---|---|
| Walk up from $u$ and $v$ with depths | any | $O(n)$ | $O(n)$ | $O(1)$ |
| Root sums and [LCA](/lowest-common-ancestor/) in $O(1)$, via the [Euler tour](/euler-tour-lca/) and a [sparse table](/sparse-table/) | group | $O(n \log n)$, or $O(n)$ | $O(1)$ | none |
| Root sums in a [Fenwick tree](/fenwick-tree/) over the [Euler tour](/euler-tour-subtree-queries/) | group | $O(n)$ | $O(\log n)$ | $O(\log n)$ point |
| [Binary lifting](/lca-binary-lifting/) with aggregates | any semigroup | $O(n \log n)$ | $O(\log n)$ | none |
| [Heavy-light decomposition](/heavy-light-decomposition/) with a [segment tree](/segment-tree/) | any monoid | $O(n)$ | $O(\log^2 n)$ | $O(\log n)$ point, $O(\log^2 n)$ path |
| [Centroid decomposition](/centroid-decomposition/) | any semigroup, static | $O(n \log n)$ | $O(\log n)$ | none |
| [Link-cut tree](/link-cut-tree/) | any monoid | $O(n)$ | $O(\log n)$ amortized | $O(\log n)$ amortized, also link and cut |
| [Tarjan's offline LCA](/tarjan-offline-lca/) with root sums | group, offline | $O((n + q)\,\alpha(n))$ in all | | none |

The centroid method stores, for each centroid $c$ and each vertex $w$ of its part, the aggregate of the path from $c$ to $w$. The path from $u$ to $v$ passes through the first centroid that separates them, so the answer is two stored aggregates.

## Bounds

- **Reading.** Each method needs $\Omega(n + q)$ time to read the tree and the queries.
- **Static semigroup queries.** For the static problem over a semigroup, with no inverse, Chazelle showed a trade-off between preprocessing and query time in which $O(n)$ preprocessing allows queries with $O(\alpha(n))$ semigroup operations, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/).
- **Dynamic sums.** A path is a tree, so the dynamic path-sum problem includes dynamic [prefix sums](/prefix-sums/). In the [cell-probe model](/cell-probe-model/), that problem needs $\Omega(\log n)$ time per operation in the worst case over updates and queries, so the $O(\log n)$ bound of the Fenwick and link-cut methods is tight in that model.
- **Space.** $\Theta(n)$ words suffice for every row of the table except the sparse table, binary lifting and the centroid method, which use $\Theta(n \log n)$; the sparse table can be replaced by an $O(n)$ structure for LCA.

## Reductions

- **To two root paths.** Through $\ell = \mathrm{lca}(u, v)$, a path query is two queries on paths that end at an ancestor, plus one value. So path queries reduce to LCA plus ancestor-path queries.
- **From range queries.** A range query on an array is a path query on the path graph with the same values, so path queries are at least as hard as [range queries](/range-sum-query/).
- **To range queries.** Heavy-light decomposition orders the vertices so that every path is $O(\log n)$ intervals, which turns a path query into $O(\log n)$ range queries. For invertible values, the Euler tour turns a root-path sum into a point query over a range-add structure.
- **LCA as a path query.** On the Euler tour, the LCA of $u$ and $v$ is the vertex of least depth between their first occurrences, a [range minimum query](/rmq-lca-equivalence/).

## Applications

- **Networks.** The bottleneck capacity of the route between two nodes of a tree network, or of a [spanning tree](/spanning-tree/) of a general network.
- **Minimum spanning trees.** The largest edge on the tree path between $u$ and $v$ decides whether a new edge $uv$ improves a minimum spanning tree, which is used in second-best spanning trees and in checking a spanning tree.
- **Dynamic graph algorithms.** Maximum-flow methods based on link-cut trees, and dynamic connectivity, use path minimum and path add on changing forests.
- **Contest and database queries.** Distances in a weighted tree, the number of distinct colours on a path, and the $k$-th vertex of a path.

## References
