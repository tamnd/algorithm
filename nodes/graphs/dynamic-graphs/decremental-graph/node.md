---
tag: MYT3AN
kind: definition
slug: decremental-graph
name: Decremental graph
aliases:
- deletions-only graph
- decremental model
area: graphs/dynamic-graphs
level: intro
summary: Only edge deletions are allowed.
prereqs: [dynamic-graph]
see_also: [incremental-graph, fully-dynamic-graph, decremental-connectivity, decremental-sssp, even-shiloach-tree, offline-dynamic-graph]
sources:
  - paper: doi:10.1145/322234.322235
    title: Shimon Even and Yossi Shiloach, An on-line edge-deletion problem, Journal of the ACM 28(1), 1 to 4 (1981)
    locator: the whole paper (deletions-only connectivity and the breadth-first levels that only grow)
  - paper: doi:10.1006/jagm.1999.1033
    title: Mikkel Thorup, Decremental dynamic connectivity, Journal of Algorithms 33(2), 229 to 243 (1999)
    locator: Section 1 (the decremental problem and the earlier bounds)
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 1 (partially dynamic problems)
  - paper: doi:10.1016/S0020-0190(97)00170-1
    title: Stephen Alstrup, Jens Peter Secher and Maz Spork, Optimal on-line decremental connectivity in trees, Information Processing Letters 64(4), 161 to 164 (1997)
    locator: the whole paper (deletions in a tree with constant-time queries)
---

A decremental graph is a [dynamic graph](/dynamic-graph/) in which every update deletes an edge (or, in some problems, a vertex, or raises an edge weight), and no update ever adds anything. Its properties change in one direction only: components split, reachable sets shrink and distances grow. Many decremental algorithms pay for their work with this one-way change, by a bound on the *total* time over all deletions. It is the mirror image of an [incremental graph](/incremental-graph/), and together the two form the partially dynamic setting.

## Definition

A **decremental graph** is a dynamic graph $G_0, G_1, \ldots, G_t$ on a fixed vertex set $V$, with $n = |V|$ and $m = |E_0|$, in which each update is $\mathrm{delete}(e)$ for an edge $e \in E_{i-1}$, so that

$$E_0 \supseteq E_1 \supseteq \cdots \supseteq E_t, \qquad |E_{i-1} \setminus E_i| = 1.$$

So $t \le m$: the sequence has at most $m$ updates. Queries about $G_i$ may come between the updates. In a weighted graph, the decremental model often also allows an update that raises the weight of an edge, because a deletion is the same as raising a weight to $\infty$. A **decremental problem** is a dynamic graph problem whose updates are of this kind; see [decremental connectivity](/decremental-connectivity/) and [decremental single-source shortest paths](/decremental-sssp/).

**Monotonicity.** If $H$ is a subgraph of $G$ on the same vertices, each path of $H$ is a path of $G$. So for all $u, v \in V$:

- $\mathrm{dist}_H(u, v) \ge \mathrm{dist}_G(u, v)$, with $\infty$ when there is no path,
- if $v$ is reachable from $u$ in $H$, then it is reachable in $G$,
- each connected component of $H$ lies inside one connected component of $G$.

Applied to $G_i \subseteq G_{i-1}$, this says that in a decremental graph distances never go down, reachability is never gained and components only split. Since $\mathrm{dist}(s, v)$ in an unweighted graph takes one of the $n + 1$ values $0, 1, \ldots, n - 1, \infty$, it can grow at most $n$ times over the whole sequence. This counting is the base of the $O(mn)$ total bound of the [Even-Shiloach tree](/even-shiloach-tree/).

The cost of a decremental algorithm is often given as a **total update time**: the time for all updates of a sequence that deletes every edge, as a function of $n$ and $m$. Dividing by $m$ gives an [amortized update time](/amortized-update-time/).

## Examples and non-examples

**Example: distances only grow.** Take $V = \{0, \ldots, 5\}$ and the 8 undirected edges $01, 02, 13, 15, 23, 24, 34, 45$, with source 0. The table gives the [breadth-first search](/breadth-first-search/) distances $(d_0, \ldots, d_5)$ after each deletion.

| deleted edge | distances from 0 |
|---|---|
| none | 0, 1, 1, 2, 2, 2 |
| 15 | 0, 1, 1, 2, 2, 3 |
| 02 | 0, 1, 3, 2, 3, 4 |
| 34 | 0, 1, 3, 2, 4, 5 |
| 13 | 0, 1, $\infty$, $\infty$, $\infty$, $\infty$ |

Each entry of each column stays the same or grows. After the last deletion, vertices 2 to 5 form a component that no longer contains 0, so the component of 0 has split.

**Example: decremental connectivity on a tree.** Delete the edges of a spanning tree one by one. Each deletion splits one component into two, so after $k$ deletions there are $k + 1$ components. Alstrup, Secher and Spork (1997) answer connectivity queries on a tree under deletions in $O(1)$ time, with $O(n)$ total update time on the word RAM.

**Example: vertex deletions.** Deleting a vertex deletes all its edges at once. Decremental problems with vertex deletions arise when a solver removes vertices that are no longer useful, for example when it prunes a graph.

**Non-example: a weight decrease.** Lowering the weight of an edge can shorten distances. An update sequence that contains a decrease is not decremental, even if it has no insertion.

**Non-example: delete and then insert again.** A sequence that deletes an edge and later inserts it again is fully dynamic. The monotone counting argument above breaks: a distance can go up and down many times, so the $O(mn)$ total bound of the Even-Shiloach tree does not hold.

## Related definitions

- **[Incremental graph](/incremental-graph/).** Only insertions. Read in reverse, a decremental sequence is incremental. So when all deletions are known in advance (the [offline](/offline-dynamic-graph/) case), a decremental connectivity instance can be solved with a [disjoint-set](/disjoint-set/) structure by inserting the edges in reverse order, in $O(m\,\alpha(n))$ total time plus the time to build the final graph. In the online case this reversal is not possible.
- **[Fully dynamic graph](/fully-dynamic-graph/).** Both insertions and deletions. Some fully dynamic algorithms keep a decremental structure and rebuild it from scratch after a number of insertions.
- **Partially dynamic.** The common name for the incremental and the decremental settings. The two are not equally hard: incremental connectivity is solved in nearly constant amortized time by a disjoint-set forest, but decremental connectivity of general graphs needs much more work; see [decremental connectivity](/decremental-connectivity/).
- **Decremental problems on directed graphs.** In a directed graph, deletions can break [strongly connected components](/strongly-connected-components/) and reachability; see [dynamic reachability](/dynamic-reachability/).

## References
