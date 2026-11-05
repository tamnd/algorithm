---
tag: JVR6G1
kind: problem
slug: dynamic-spanner
name: Dynamic spanner
aliases:
- fully dynamic spanner
area: graphs/dynamic-graphs
level: research
summary: Maintain a sparse subgraph that approximately preserves distances under updates.
prereqs: [dynamic-graph, girth, breadth-first-search]
see_also: [geometric-spanner, dynamic-all-pairs-shortest-paths, decremental-sssp, dynamic-minimum-spanning-tree, dynamic-connectivity, amortized-update-time]
sources:
  - paper: doi:10.1007/bf02189308
    title: Ingo Althöfer, Gautam Das, David Dobkin, Deborah Joseph and José Soares, On sparse spanners of weighted graphs, Discrete and Computational Geometry 9(1), 81 to 100 (1993)
    locator: the greedy spanner and the girth argument for its size
  - paper: doi:10.1002/rsa.20130
    title: Surender Baswana and Sandeep Sen, A simple and linear time randomized algorithm for computing sparse spanners in weighted graphs, Random Structures and Algorithms 30(4), 532 to 563 (2007)
    locator: the clustering algorithm for (2k - 1)-spanners with O(k n^(1 + 1/k)) expected edges
  - paper: doi:10.1145/2344422.2344425
    title: Surender Baswana, Sumeet Khurana and Soumojit Sarkar, Fully dynamic randomized algorithms for graph spanners, ACM Transactions on Algorithms 8(4), 1 to 51 (2012)
    locator: the two fully dynamic algorithms (expected amortized update time, oblivious adversary)
  - paper: doi:10.1145/1921659.1921666
    title: Michael Elkin, Streaming and fully dynamic centralized algorithms for constructing and maintaining sparse spanners, ACM Transactions on Algorithms 7(2), 1 to 17 (2011)
    locator: the fully dynamic centralized algorithm
  - paper: doi:10.1109/focs.2016.44
    title: Ittai Abraham, David Durfee, Ioannis Koutis, Sebastian Krinninger and Richard Peng, On fully dynamic graph sparsifiers, Proceedings of FOCS 2016, 335 to 344
    locator: the dynamic spanner subroutine and its use for spectral sparsifiers
---

The dynamic spanner problem asks to keep a $t$-spanner of an undirected [dynamic graph](/dynamic-graph/): a subgraph $H$ of $G$ such that, for every pair of vertices, the distance in $H$ is at most $t$ times the distance in $G$. The goal is a spanner with few edges, usually $O(n^{1 + 1/k})$ edges for stretch $t = 2k - 1$, and a small update time. For an unweighted graph, randomized algorithms keep such a spanner, up to small factors in the size, in expected amortized time that is constant or polylogarithmic for a fixed $k$ against an oblivious adversary. Spanners are building blocks of dynamic algorithms for approximate distances and for sparsifiers.

## In plain words

A road network has far more roads than needed for travel. Keep only a few roads, so that every trip in the small network is at most a few times longer than the shortest trip in the full one. Roads open and close, and the small network must keep this promise.

A new road that is already well covered by kept roads can be ignored. A new road between places that are far apart in the kept network must be kept. When a kept road closes, some trips get too long, and other roads must be brought back in. The hard part is to find those quickly, without checking every road.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices, unweighted or with positive weights, a stretch $t \ge 1$, and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates.

**Output.** After each update, a subgraph $H = (V, E_H)$ with $E_H \subseteq E$ such that $d_H(x, y) \le t \cdot d_G(x, y)$ for all $x, y \in V$. It is enough to check this for the edges of $G$: if $d_H(u, v) \le t \cdot w(u, v)$ for each edge $\{u, v\}$ of $G$, then each shortest path of $G$ can be replaced edge by edge.

**Cost.** The size $|E_H|$, the update time, worst case or [amortized](/amortized-update-time/), and the **recourse**, the number of changes to $E_H$ per update. Randomized algorithms state whether the adversary is oblivious or adaptive.

**Size and stretch.** Every graph has a $(2k - 1)$-spanner with $O(n^{1 + 1/k})$ edges. In a graph of [girth](/girth/) more than $2k$, removing any edge $\{u, v\}$ leaves $u$ and $v$ at distance at least $2k$, so its only $(2k - 1)$-spanner is the graph itself, and the girth conjecture of Erdős states that such graphs with $\Omega(n^{1 + 1/k})$ edges exist. So $2k - 1$ and $n^{1 + 1/k}$ are the expected trade-off.

## Variants

- **Insertions only, deletions only, fully dynamic.**
- **Weighted.** Positive edge weights; many dynamic results first treat the unweighted case and then group weights into powers of 2.
- **Additive spanners.** $d_H(x, y) \le d_G(x, y) + \beta$.
- **Adaptive adversary.** The updates may depend on the current spanner. Randomized algorithms against an oblivious adversary need not work here.
- **Low recourse.** Few changes to $H$ per update, which matters when $H$ feeds another dynamic algorithm.
- **Geometric.** The vertices are points and the edge weights are distances; see [geometric spanners](/geometric-spanner/).

## Examples

Take $V = \{0, \ldots, 5\}$ and stretch $t = 3$. The rule: on an insertion of $\{u, v\}$, add it to $H$ if $d_H(u, v) > 3$. On a deletion of an edge of $H$, remove it and then add each edge of $G$ whose ends are now more than 3 apart in $H$.

| update | action | $\lvert E \rvert$ | $\lvert E_H \rvert$ |
|---|---|---|---|
| insert 01, 12, 23 | added | 3 | 3 |
| insert 30 | skipped, $d_H = 3$ | 4 | 3 |
| insert 02 | skipped, $d_H = 2$ | 5 | 3 |
| insert 13 | skipped, $d_H = 2$ | 6 | 3 |
| insert 34, 45, 50 | added | 9 | 6 |
| insert 24 | skipped, $d_H = 2$ | 10 | 6 |
| delete 01 | removed, then 02 added, since $d_H(0, 2)$ became 4 | 9 | 6 |
| delete 34 | removed, nothing added | 8 | 5 |

After the insertions, $H$ is the 6-cycle $0, 1, 2, 3, 4, 5$, with 6 of the 10 edges. The deletion of $01$ breaks the guarantee for edge $02$ only, and the repair adds that edge. The deletion of $34$ needs no repair: edge $24$ still has the path $2, 0, 5, 4$ of length 3. This rule keeps an invariant: an edge enters $H$ only when its ends are more than $t$ apart in $H$, so it closes no cycle of at most $t + 1$ edges, and deletions do not create cycles. So $H$ always has girth more than $t + 1$, and for $t = 2k - 1$ this bounds $|E_H|$ by $O(n^{1 + 1/k})$. The cost is in the repair: finding the edges that a deletion leaves uncovered is the hard part.

## Known algorithms

**Static.** The greedy algorithm of Althöfer et al. scans the edges by weight and keeps an edge if its ends are more than $2k - 1$ apart in the current spanner. The result has girth more than $2k$, so it has $O(n^{1 + 1/k})$ edges. Baswana and Sen (2007) build a $(2k - 1)$-spanner with $O(k n^{1 + 1/k})$ expected edges in $O(k m)$ expected time by $k$ rounds of random clustering.

| setting | algorithm | update time | case |
|---|---|---|---|
| any | recompute with Baswana and Sen | $O(k m)$ | expected |
| insertions only | greedy rule above | one search of depth $2k - 1$ in $H$, $O(n^{1 + 1/k})$ | worst, deterministic |
| fully dynamic | Elkin (2007, 2011) | small for insertions, larger for deletions | expected, randomized |
| fully dynamic | Baswana, Khurana and Sarkar (2006, 2012) | constant or polylogarithmic for fixed $k$ | expected amortized, oblivious adversary |

**Dynamic clustering.** Baswana, Khurana and Sarkar keep the random clusters of the Baswana-Sen algorithm under updates. A deletion inside a cluster can break it, but since the cluster centers are random and the adversary does not see them, such deletions are rare, and the cost of rebuilding is paid for by the many updates before. They give two algorithms with different trade-offs between the update time and the size, with expected spanner size $O(k n^{1 + 1/k})$ up to a logarithmic factor.

**Spanners as tools.** Abraham, Durfee, Koutis, Krinninger and Peng (2016) keep several disjoint spanners dynamically and use them to keep spectral sparsifiers, which shows how a dynamic spanner feeds other dynamic structures.

## Bounds

**Size.** For stretch $2k - 1$, $\Omega(n^{1 + 1/k})$ edges are needed on some graphs if the girth conjecture holds, already in the static case.

**Time.** For a fixed $k$, expected amortized update time that is constant or polylogarithmic in $n$ is possible against an oblivious adversary. Bounds that are worst case, deterministic, or against an adaptive adversary are weaker, and are a topic of current work.

## Reductions

- **To approximate distances.** A $t$-spanner $H$ with few edges lets a static distance algorithm, run on $H$, give $t$-approximate distances faster. So a dynamic spanner turns a static algorithm into a dynamic one with a smaller graph.
- **To connectivity.** Any spanner with finite stretch has the same components as $G$, so it contains a spanning forest; a spanner is a stronger certificate.
- **To sparsifiers.** A union of disjoint spanners is the core of some cut and spectral sparsifier constructions.

## Applications

- **Approximate distance oracles.** Dynamic structures that answer approximate distance queries keep a sparse spanner and run searches on it.
- **Networks.** Routing tables and overlay networks keep a sparse set of links that keeps routes short as links change.
- **Subroutine.** Dynamic sparsifiers, approximate shortest paths and some flow algorithms work on a dynamic spanner instead of the whole graph.

## References
