---
tag: ZS0KCA
kind: algorithm
slug: frederickson-topology-trees
name: Frederickson's topology trees
aliases:
- topology trees
area: graphs/dynamic-graphs
level: research
summary: Hierarchical partition of a spanning forest that supports dynamic minimum spanning tree updates.
solves: [dynamic-minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m^(1/2))}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [minimum-spanning-tree, spanning-forest, fully-dynamic-graph]
see_also: [eppstein-galil-italiano-nissenzweig, sparsification, top-tree, rake-compress-tree, holm-de-lichtenberg-thorup, worst-case-update-time, cycle-property, cut-property]
sources:
  - paper: doi:10.1137/0214055
    title: Greg N. Frederickson, Data structures for on-line updating of minimum spanning trees, with applications, SIAM Journal on Computing 14(4), 781 to 798 (1985)
    locator: the whole paper (clusters of a spanning tree of degree at most three, the topology tree and the two-dimensional topology tree, O(m^(1/2)) worst-case time per update, and the O(m^(2/3)) one-level method as a first step)
  - paper: doi:10.1137/S0097539792226825
    title: Greg N. Frederickson, Ambivalent data structures for dynamic 2-edge-connectivity and k smallest spanning trees, SIAM Journal on Computing 26(2), 484 to 538 (1997)
    locator: the sections on restricted multilevel partitions and topology trees, used for 2-edge connectivity
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 3 (Frederickson's structure as the inner algorithm, giving O(n^(1/2)) per update)
---

Frederickson's topology trees keep the [minimum spanning forest](/minimum-spanning-tree/) of a graph under edge insertions and deletions in $O(m^{1/2})$ worst-case time per update, deterministically; this was the first fully dynamic algorithm for the problem with sublinear update time. The forest is cut into connected **clusters** of about $z$ vertices, after a change that gives every vertex degree at most three, and a table keeps, for each pair of clusters, the lightest non-tree edge between them. When a forest edge is deleted, the replacement is the lightest table entry between the clusters on the two sides. With one level of clusters this costs $O(m^{2/3})$; the **topology tree** builds the clusters into a balanced hierarchy, and the **two-dimensional topology tree** keeps the minima over pairs of clusters of all levels, which lowers the cost to $O(m^{1/2})$. Frederickson presented it at STOC 1983 and in the SIAM Journal on Computing in 1985.

## In plain words

The cheapest network that connects all points of a graph is a tree, or a forest if the graph falls apart. When a link of that tree breaks, the tree splits in two, and the cheapest spare link between the two halves must be found.

Looking at every spare link is slow. So cut the tree into chunks of roughly equal size, and for every pair of chunks remember the cheapest spare link between them. After a break, only the chunk that held the broken link changes, and the search looks at pairs of chunks instead of single links.

A tree of chunks inside chunks makes the search faster still, because a big pair can be answered by its two halves.

## The problem

The input is a graph on $n$ vertices with real edge weights and a sequence of updates: insert an edge with a weight, or delete an edge. After each update the algorithm must hold the minimum spanning forest $F$ of the current graph. Ties are broken by the order (weight, smaller end, larger end), so $F$ is unique. This is the fully dynamic form of the [dynamic minimum spanning tree](/dynamic-minimum-spanning-tree/) problem; a weight change is a deletion followed by an insertion.

Two classic facts decide every update. By the [cycle property](/cycle-property/), a new edge joins $F$ exactly when it is lighter than the heaviest edge on the forest path between its ends, and then that heaviest edge leaves. By the [cut property](/cut-property/), when a forest edge is deleted, the new forest takes the lightest non-tree edge across the cut between the two parts, if one exists.

## The algorithm

**Degree three.** Frederickson first replaces each vertex of high degree by a path of copies joined by edges of weight $-\infty$, so that every vertex has degree at most three and the graph has $O(m)$ vertices. Then a cluster of $z$ vertices has at most $3z$ edges leaving it, and a split or a join of clusters touches $O(z)$ edges.

**Clusters.** The forest $F$ is partitioned into vertex sets that are connected in $F$, each of size between $z$ and $3z - 2$ in the paper (a whole small tree may be smaller). The **cluster tree** has one node per cluster and one edge per forest edge between two clusters. For each pair of clusters $(a, b)$, the **table** keeps the lightest non-tree edge with one end in $a$ and one in $b$.

```pseudo id=main
INSERT(u, v, w)
L1  if u and v are in different trees of F: add (u, v) to F; join two small clusters if they fit
L2  else x ← the heaviest edge of F on the path from u to v, found along the cluster path
L3      if (u, v) is lighter than x: move x from F to the table and add (u, v) to F; else put (u, v) in the table

DELETE(u, v)                                   ▷ a non-tree edge is only removed from the table
L4  remove (u, v) from F; if it was inside a cluster, split that cluster into its two connected parts
L5  for each cluster a on the side of u and b on the side of v: look at the table entry (a, b)
L6  if an entry was found, move the lightest one from the table to F

AFTER EVERY z UPDATES (this implementation)
L7  recompute the clusters, the cluster tree and the table

BUILD-TOPOLOGY-TREE(a tree of degree at most 3)
L8  level 0 has one cluster per vertex; repeat while two clusters can be joined:
L9      choose a maximal set of disjoint pairs of adjacent clusters, each with one cluster of external degree 1 or both of degree at most 2
L10     the next level has one cluster per chosen pair and a copy of every other cluster
```

Lines L1 to L3 apply the cycle property. Line L4 splits a cluster in $O(z)$ time with degree three. Line L5 is the search of the cut property: the clusters of each side are found by a walk in the cluster tree, and with $k = O(m/z)$ clusters there are $O(k^2)$ pairs. The table changes by $O(z)$ entries when a cluster is split or joined, because only the edges at its vertices change their pair.

**Topology tree.** Lines L8 to L10 build the restricted multilevel partition of Frederickson: each cluster at level $i$ is one or two adjacent clusters at level $i - 1$, external degrees stay at most three, and the number of clusters falls by a constant factor per level, so there are $O(\log n)$ levels. The **topology tree** has one node per cluster of each level, with the clusters it joins as children. An update to the forest changes $O(1)$ clusters per level, so the topology tree is repaired in $O(\log n)$ time after its base clusters change.

**Two-dimensional topology tree.** For every pair of topology tree nodes $(a, b)$ at the same level, keep the lightest non-tree edge between the clusters $a$ and $b$; the entry of $(a, b)$ is the minimum of the up to four entries of the pairs of their children. The search of line L5 then descends from the pair of the two roots of the sides and needs $O(m/z)$ entries in place of $O((m/z)^2)$, and an update repairs $O(m/z)$ entries along the paths of the changed clusters.

## Example

**Updates.** Take $K_4$ with the weights $w(01) = 1$, $w(12) = 2$, $w(23) = 3$, $w(03) = 4$, $w(02) = 5$, $w(13) = 6$, inserted in the order 01, 02, 03, 12, 13, 23, with $z = \lceil 4^{2/3} \rceil = 3$ as in the implementation.

| update | forest $F$ | clusters | table |
|---|---|---|---|
| insert 01, 02, 03 | 01, 02, 03 | $\{0, 1, 2\}$, $\{3\}$ | empty |
| insert 12 (2) | 01, 03, 12 | $\{0, 1, 2\}$, $\{3\}$ | 02 |
| insert 13 (6) | 01, 03, 12 | $\{0, 1, 2\}$, $\{3\}$ | 02, 13 |
| insert 23 (3) | 01, 12, 23 | after re-clustering: $X = \{1, 2, 3\}$, $Y = \{0\}$ | $(X, Y)$: 02, 03; $(X, X)$: 13 |
| delete 12 | 01, 23, 03 | $\{0, 2, 3\}$, $\{1\}$ | $(\{0, 2, 3\}, \{1\})$: 13; inside $\{0, 2, 3\}$: 02 |

Inserting 12 closes the cycle 0, 1, 2, whose heaviest edge 02 (5) leaves $F$ for the table. Inserting 13 closes the cycle 1, 0, 3 with heaviest edge 13 itself, so 13 goes to the table. Inserting 23 closes the cycle 2, 1, 0, 3 with heaviest edge 03 (4), which leaves $F$. The deletion of 12 splits $X$ into $C = \{1\}$ and $X' = \{2, 3\}$. The side of 1 has the clusters $Y$ and $C$, the side of 2 has $X'$, and the pairs $(Y, X')$ with 02 and 03 and $(C, X')$ with 13 give the lightest edge 03 (4). It joins $F$, and the clusters $\{0\}$ and $\{2, 3\}$ are then joined because together they have $3 \le z$ vertices.

**Topology tree.** For the tree with edges 01, 12, 23, 14, 45, 56, 57, where the vertices 1 and 5 have degree three, the levels are:

| level | clusters |
|---|---|
| 0 | $\{0\}, \{1\}, \ldots, \{7\}$ |
| 1 | $\{0, 1\}$, $\{2, 3\}$, $\{4\}$, $\{5, 6\}$, $\{7\}$ |
| 2 | $\{0, 1, 2, 3\}$, $\{4, 5, 6\}$, $\{7\}$ |
| 3 | $\{0, \ldots, 6\}$, $\{7\}$ |
| 4 | $\{0, \ldots, 7\}$ |

At level 1, the cluster $\{1\}$ of degree three is joined with its neighbor $\{0\}$ of degree one, and $\{4\}$ is left alone: its neighbor $\{1\}$ is already taken, and its other neighbor $\{5\}$ has degree three, so the pair is not allowed. $\{7\}$ is left alone because $\{5\}$ is joined with $\{6\}$ first.

## Correctness

The algorithm keeps two invariants: $F$ is the minimum spanning forest of the current graph, and the table holds exactly the non-tree edges, each under the pair of clusters of its ends. An insertion between two trees adds an edge across a cut with no other crossing edge, so it belongs to the forest; an insertion inside a tree is decided by the cycle property on the unique forest path. A deletion of a forest edge leaves two trees $T_u$ and $T_v$; by the cut property the new forest adds the lightest non-tree edge across, and every edge across has its ends in a cluster of $T_u$ and a cluster of $T_v$, so line L5 sees it. Splits, joins and re-clustering move each non-tree edge to its new pair. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **One level.** With degree three and $O(m)$ vertices, there are $k = O(m/z)$ clusters. A split or join costs $O(z)$, the path maximum costs $O(z + k)$ with a walk along the cluster path, and the search costs $O(k^2)$. With $z = m^{2/3}$ every update takes $O(m^{2/3})$ time in the worst case.
- **Topology trees.** With the two-dimensional topology tree the search costs $O(m/z)$ and the cluster changes $O(z)$, so $z = m^{1/2}$ gives $O(m^{1/2})$ worst-case time per update. Clusters are kept within their size bounds by local splits and joins, so no update is slow.
- **Space.** $O(m)$: the two-dimensional topology tree has $O(k^2) = O(m)$ entries when $z = m^{1/2}$.
- **With sparsification.** Run on graphs of $O(n)$ edges inside [sparsification](/sparsification/), the bound becomes $O(n^{1/2})$; see the [Eppstein-Galil-Italiano-Nissenzweig algorithm](/eppstein-galil-italiano-nissenzweig/).
- **This implementation.** It keeps the one-level table without the degree reduction, uses $z = \lceil n^{2/3} \rceil$, and rebuilds the clusters every $z$ updates, so its bounds are amortized and depend on the degrees; it checks the method against Kruskal's algorithm, not the time bound.
- **Kind of bound.** Worst case per update, deterministic.

## Properties

- **Fully dynamic.** Insertions, deletions and weight changes.
- **Worst case and deterministic.** No amortization and no random choices, so the bound holds against an [adaptive adversary](/adaptive-adversary/).
- **Online.** Each update is finished before the next one is read.
- **Degree three.** The analysis needs bounded degree; the reduction to degree three is part of the method.

## Variants and improvements

- **Sparsification.** Eppstein, Galil, Italiano and Nissenzweig (1997) use the method on node graphs of $O(n)$ edges and get $O(n^{1/2})$ worst-case time.
- **2-edge connectivity and $k$ smallest spanning trees.** Frederickson (1997) extended topology trees with **ambivalent** data structures, which keep several candidate answers at each node, to fully dynamic 2-edge connectivity in $O(m^{1/2})$ time per update and to the $k$ smallest spanning trees.
- **Top trees.** [Top trees](/top-tree/) of Alstrup, Holm, de Lichtenberg and Thorup generalize the clusters to arbitrary degree and offer a general interface; their worst-case implementation uses topology trees.
- **Amortized polylogarithmic.** The [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/) gives $O(\log^4 n)$ amortized time for minimum spanning forests.
- **Rake-compress trees.** [RC-trees](/rake-compress-tree/) build a similar hierarchy by randomized contraction.

## When to use it

Topology trees matter mainly as the source of the cluster idea and as the first sublinear worst-case bound. For dynamic minimum spanning forests with guaranteed time per update, combine them with sparsification. In practice, simpler methods are often fast enough: recomputation with Kruskal's algorithm on small graphs, or a [link-cut tree](/link-cut-tree/) when edges are only inserted. When amortized time is fine, the polylogarithmic algorithms are faster on large graphs.

## Pitfalls

- **High degree.** Without the reduction to degree three, a cluster may have many edges leaving it, and a split of a cluster can change many table entries.
- **Stale table entries.** When a cluster splits or joins, every non-tree edge at its vertices must move to its new pair; otherwise the search of line L5 misses an edge or returns one inside a side.
- **Ties.** Without a fixed tie order, the forest is not unique, and different parts of the structure may disagree on which edge is heaviest.
- **Small trees.** A tree of fewer than $z$ vertices is a single cluster below the lower size bound; the size rules must allow it.
- **Inserting a heavy edge inside a tree.** The new edge goes to the table, not to the forest, and the forest does not change.

## Implementations

## History

Frederickson presented topology trees at STOC 1983 and published the full paper in 1985. It gave the first fully dynamic minimum spanning tree algorithm with sublinear time per update, $O(m^{1/2})$ in the worst case, against $O(m)$ for recomputation, and it introduced the clusters and multilevel partitions that later appeared in top trees and RC-trees. Eppstein, Galil, Italiano and Nissenzweig (1992, journal 1997) lowered the bound to $O(n^{1/2})$ with sparsification. Frederickson extended the structure to 2-edge connectivity in 1991, with the journal version in 1997.

## References
