---
tag: 7Y8SYW
kind: problem
slug: dynamic-connectivity
name: Dynamic connectivity
aliases:
- fully dynamic connectivity
- dynamic connected components
area: graphs/dynamic-graphs
level: advanced
summary: Maintain connected components under edge insertions and deletions and answer connectivity queries.
prereqs: [dynamic-graph, connected-components, spanning-forest, amortized-update-time]
see_also: [holm-de-lichtenberg-thorup, incremental-connectivity, decremental-connectivity, offline-dynamic-connectivity, dynamic-connectivity-lower-bound, euler-tour-tree, dynamic-minimum-spanning-tree, sparsification]
sources:
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 1 (history and results) and Section 2 (the connectivity algorithm with edge levels)
  - paper: doi:10.1145/320211.320215
    title: Monika R. Henzinger and Valerie King, Randomized fully dynamic graph algorithms with polylogarithmic time per operation, Journal of the ACM 46(4), 502 to 516 (1999)
    locator: the connectivity algorithm and its expected amortized bound
  - paper: doi:10.1137/0214055
    title: Greg N. Frederickson, Data structures for on-line updating of minimum spanning trees, with applications, SIAM Journal on Computing 14(4), 781 to 798 (1985)
    locator: the whole paper (O(m^(1/2)) worst-case time per update with topology trees)
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: the results for connectivity (O(n^(1/2)) worst-case time per update)
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Patrascu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: Section 1 (the lower bound for dynamic connectivity)
  - paper: doi:10.1137/1.9781611973105.81
    title: Bruce M. Kapron, Valerie King and Ben Mountjoy, Dynamic graph connectivity in polylogarithmic worst case time, Proceedings of SODA 2013, 1131 to 1142
    locator: Section 1 (the main result, a Monte Carlo algorithm with polylogarithmic worst-case update time)
  - paper: doi:10.1145/335305.335345
    title: Mikkel Thorup, Near-optimal fully-dynamic graph connectivity, Proceedings of STOC 2000, 343 to 350
    locator: the main result (O(log n (log log n)^3) expected amortized update time)
  - paper: doi:10.1137/1.9781611973105.126
    title: Christian Wulff-Nilsen, Faster deterministic fully-dynamic graph connectivity, Proceedings of SODA 2013, 1757 to 1769
    locator: the main result (O(log^2 n / log log n) amortized deterministic update time)
  - paper: doi:10.46298/theoretics.23.6
    title: Shang-En Huang, Dawei Huang, Tsvi Kopelowitz, Seth Pettie and Mikkel Thorup, Fully dynamic connectivity in O(log n (log log n)^2) amortized expected time, TheoretiCS 2 (2023); first version in SODA 2017
    locator: the main theorem
---

Dynamic connectivity is the problem of keeping the [connected components](/connected-components/) of an undirected [dynamic graph](/dynamic-graph/) under edge insertions and deletions, so that a query "are $u$ and $v$ connected?" can be answered at any time. With insertions only, a [disjoint-set](/disjoint-set/) structure solves it in nearly constant time per operation. Deletions make it much harder, because a deletion can split a component, and no union-find structure can undo a merge cheaply. The fully dynamic problem is solved in polylogarithmic amortized time per update, and a cell-probe lower bound shows that $\Omega(\log n)$ is necessary.

## In plain words

Think of a road network in which roads open and close. At any moment someone asks whether one town can still reach another. Recomputing the whole map after every change is slow.

Opening a road is easy: two groups of towns become one group. Closing a road is the hard case. If some other road still links the two sides, nothing changes. If not, one group falls into two. To tell which case holds, the program must look for another road between the two sides, and it must do this without looking at every road each time.

The good methods keep a skeleton of the network, a set of roads with no loops that still connects every group. Closing a road outside the skeleton changes nothing. Closing a skeleton road starts a search for a replacement road.

## Definition

**Input.** A number $n$ of vertices $V = \{1, \ldots, n\}$ and an online sequence of operations on an undirected graph $G = (V, E)$, which starts with $E = \emptyset$:

- $\mathrm{insert}(u, v)$ adds the edge $\{u, v\}$ to $E$,
- $\mathrm{delete}(u, v)$ removes the edge $\{u, v\}$ from $E$, if it is there,
- $\mathrm{connected}(u, v)$ returns true if and only if $G$ has a path from $u$ to $v$ in its current state.

**Output.** The answer to each query, where each answer must be given before the next operation is read.

**Cost.** The update time $t_u$ and the query time $t_q$, as functions of $n$ (and sometimes of the current number of edges $m$). Each bound is worst case, amortized or expected; see [amortized update time](/amortized-update-time/). This is the **fully dynamic** problem. A multigraph is allowed in most algorithms, so the same pair may be inserted twice.

## Variants

- **Incremental.** Insertions only; see [incremental connectivity](/incremental-connectivity/). A disjoint-set forest gives $O(\alpha(n))$ amortized time per operation.
- **Decremental.** Deletions only; see [decremental connectivity](/decremental-connectivity/).
- **Offline.** The whole sequence is known in advance; see [offline dynamic connectivity](/offline-dynamic-connectivity/). Divide and conquer over time with a [union-find with rollback](/union-find-with-rollback/) solves it with $O(\log q)$ union-find operations per graph operation, where $q$ is the length of the sequence, so in $O(\log q \log n)$ time per operation.
- **Dynamic forests.** If the graph stays a forest, [Euler tour trees](/euler-tour-tree/) or [link-cut trees](/link-cut-tree/) answer each operation in $O(\log n)$ time; see [dynamic tree](/dynamic-tree/).
- **Counting.** Maintain the number of components. It changes by one exactly when an insertion joins two components or a deletion splits one, so any connectivity structure that detects these events also maintains the count.
- **Higher connectivity.** Keep bridges, 2-edge-connected components or biconnected components; see [dynamic biconnectivity](/dynamic-biconnectivity/).
- **Directed graphs.** The directed analogue is [dynamic reachability](/dynamic-reachability/), which is believed to be much harder.
- **Special graph classes.** For planar graphs with a fixed embedding, and for graphs with a bounded number of edges, faster or simpler structures exist.

## Examples

**One sequence.** On $V = \{0, \ldots, 5\}$, the sequence insert(0, 1), insert(1, 2), insert(3, 4), connected(0, 2), delete(1, 2), connected(0, 2) answers yes and then no. The full trace with the number of components is on the [dynamic graph](/dynamic-graph/) page.

**Tree edges and replacement edges.** Let $G$ have 7 vertices and the edges $01, 12, 20, 23, 34, 45, 53, 16$. A spanning forest $F$ built in this edge order takes the tree edges $01, 12, 23, 34, 45, 16$. The non-tree edges are $20$ and $53$.

| deleted edge | kind | the two sides of $F$ | replacement edge | components after |
|---|---|---|---|---|
| 20 | non-tree | none | none needed | 1 |
| 34 | tree | $\{0, 1, 2, 3, 6\}$ and $\{4, 5\}$ | 53 | 1 |
| 23 | tree | $\{0, 1, 2, 6\}$ and $\{3, 4, 5\}$ | none | 2 |
| 16 | tree | $\{0, \ldots, 5\}$ and $\{6\}$ | none | 2 |

Each row is a separate deletion from the full graph $G$. Deleting a non-tree edge never changes connectivity. Deleting a tree edge splits a tree of $F$ into two parts, and the component stays whole exactly when some non-tree edge has one end in each part. In the second row, edge 53 joins the parts, so it becomes a tree edge.

**A bad case for naive search.** Keep $F$ and, after deleting a tree edge, scan all non-tree edges for a replacement. On a long path with many extra edges inside one end, an adversary can make each deletion of a tree edge scan $\Theta(m)$ non-tree edges. The algorithms below avoid this by scanning from the smaller side and by charging each scanned edge to a bounded counter.

## Known algorithms

All bounds are for $n$ vertices, with $m$ the current number of edges. "Query" is the time of $\mathrm{connected}(u, v)$.

| algorithm | update time | query time | case | deterministic |
|---|---|---|---|---|
| recompute with search after each update | $O(n + m)$ | $O(1)$ | worst | yes |
| [Frederickson](/frederickson-topology-trees/) (1985), topology trees | $O(m^{1/2})$ | $O(1)$ | worst | yes |
| [sparsification](/sparsification/) over Frederickson ([EGIN](/eppstein-galil-italiano-nissenzweig/), 1997) | $O(n^{1/2})$ | $O(1)$ | worst | yes |
| Henzinger and King (1999) | $O(\log^3 n)$ | $O(\log n / \log\log n)$ | expected amortized | no, Las Vegas |
| [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/) (2001) | $O(\log^2 n)$ | $O(\log n / \log\log n)$ | amortized | yes |
| Kapron, King and Mountjoy (2013) | polylogarithmic | polylogarithmic | worst | no, Monte Carlo |

The Holm, de Lichtenberg and Thorup algorithm is the standard one. It gives each edge a level between 0 and $\lfloor \log_2 n \rfloor$ and keeps one spanning forest per level in Euler tour trees. A level only goes up, and a tree at level $i$ has at most $n / 2^i$ vertices. When a tree edge is deleted, the search for a replacement looks at the smaller side, and each edge that it looks at and rejects moves up one level. Since each edge can move up at most $\log_2 n$ times, and each move costs $O(\log n)$ in the Euler tour trees, the total cost is $O(\log^2 n)$ per update in the amortized sense. Later work lowered the amortized bound: Thorup (2000) to $O(\log n (\log\log n)^3)$ expected, Wulff-Nilsen (2013) to $O(\log^2 n / \log\log n)$ deterministic, and Huang, Huang, Kopelowitz, Pettie and Thorup (2017) to $O(\log n (\log\log n)^2)$ expected.

## Bounds

**Upper bound.** $O(\log^2 n)$ amortized deterministic update time with $O(\log n / \log\log n)$ query time (Holm, de Lichtenberg and Thorup), and $O(\log n (\log\log n)^2)$ expected amortized with a randomized algorithm. For worst-case bounds, polylogarithmic time is possible with a Monte Carlo algorithm (Kapron, King and Mountjoy), whose answers are correct with high probability against an [oblivious adversary](/oblivious-adversary/). Deterministic worst-case bounds are much weaker; $O(n^{1/2})$ by sparsification held for a long time.

**Lower bound.** Pătraşcu and Demaine (2006) proved, in the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ bits, that any structure for dynamic connectivity has $\max(t_u, t_q) = \Omega(\log n)$ in the amortized sense. They also proved the trade-offs $t_q \lg(t_u / t_q) = \Omega(\log n)$ and $t_u \lg(t_q / t_u) = \Omega(\log n)$. The bound holds even when the graph is a union of paths. So the gap between the best upper bound and the lower bound is a factor of $O((\log\log n)^2)$ for randomized algorithms. See [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/).

**Why deletions are the hard part.** An insertion changes the components only by merging two of them. A deletion of a tree edge must decide whether a replacement edge exists, and this is a search over the edges between the two sides of a cut. All the known fast algorithms are ways to bound this search.

## Reductions

- **From connectivity to minimum spanning forest.** Give every edge weight 1 and keep a [minimum spanning forest](/dynamic-minimum-spanning-tree/). Two vertices are connected if and only if they are in the same tree of the forest. So dynamic connectivity is no harder than dynamic minimum spanning forest, up to the cost of a tree query.
- **Bipartiteness through the double cover.** A graph is bipartite exactly when no vertex $v$ has its two copies $v_0$ and $v_1$ connected in the bipartite double cover; see [dynamic bipartiteness](/dynamic-bipartiteness/). The level structure of Holm, de Lichtenberg and Thorup also gives polylogarithmic bounds for minimum spanning forests, 2-edge connectivity and biconnectivity.
- **From dynamic forests.** Dynamic connectivity on forests is a special case, so the $\Omega(\log n)$ lower bound applies to [link-cut trees](/link-cut-tree/) and Euler tour trees too.

## Applications

- **Network monitoring.** Track whether parts of a network stay connected as links fail and come back.
- **Subroutine in other dynamic algorithms.** Dynamic minimum spanning forest, 2-edge connectivity, biconnectivity and bipartiteness are built on the same level structure.
- **Static algorithms that delete edges.** Some algorithms for cuts and for graph decompositions repeatedly delete edges and ask whether the graph is still connected. A dynamic connectivity structure replaces a full search per deletion.
- **Geometry and simulation.** Keep the connected groups of moving objects, where two objects are linked when they are close.

## References
