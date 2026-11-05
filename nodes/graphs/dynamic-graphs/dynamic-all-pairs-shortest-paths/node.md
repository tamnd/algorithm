---
tag: R2C0JF
kind: problem
slug: dynamic-all-pairs-shortest-paths
name: Dynamic all-pairs shortest paths
aliases:
- dynamic APSP
area: graphs/dynamic-graphs
level: research
summary: Maintain all-pairs shortest-path distances under edge updates.
prereqs: [all-pairs-shortest-paths, dynamic-single-source-shortest-paths, floyd-warshall]
see_also: [demetrescu-italiano-apsp, decremental-sssp, dynamic-transitive-closure, even-shiloach-tree, johnson, omv-conjecture]
sources:
  - paper: doi:10.1145/1039488.1039492
    title: Camil Demetrescu and Giuseppe F. Italiano, A new approach to dynamic all pairs shortest paths, Journal of the ACM 51(6), 968 to 992 (2004)
    locator: the main theorem (O(n^2 log^3 n) amortized time per vertex update, O(1) query time) and the introduction (the history of the problem)
  - paper: doi:10.1007/978-3-540-27810-8_33
    title: Mikkel Thorup, Fully-dynamic all-pairs shortest paths, faster and allowing negative cycles, Proceedings of SWAT 2004, Lecture Notes in Computer Science 3111, 384 to 396
    locator: the main theorem (a smaller polylogarithmic factor, and negative weights)
  - paper: doi:10.1145/1060590.1060607
    title: Mikkel Thorup, Worst-case update times for fully-dynamic all-pairs shortest paths, Proceedings of STOC 2005, 112 to 119
    locator: the main theorem (subcubic worst-case update time)
  - paper: doi:10.1137/1.9781611974782.28
    title: Ittai Abraham, Shiri Chechik and Sebastian Krinninger, Fully dynamic all-pairs shortest paths with worst-case update-time revisited, Proceedings of SODA 2017, 440 to 452
    locator: the main theorem (randomized worst-case update time)
  - paper: doi:10.1109/SFFCS.1999.814580
    title: Valerie King, Fully dynamic algorithms for maintaining all-pairs shortest paths and transitive closure in digraphs, Proceedings of FOCS 1999, 81 to 89
    locator: the fully dynamic algorithm for small integer weights
---

The dynamic all-pairs shortest paths problem asks to keep the distance $d(x, y)$ between every pair of vertices of a weighted directed [dynamic graph](/dynamic-graph/) while edges change. The static problem is [all-pairs shortest paths](/all-pairs-shortest-paths/), solved in $O(n^3)$ time by [Floyd-Warshall](/floyd-warshall/), so recomputation costs $O(n^3)$ per update. A single update can change $\Theta(n^2)$ distances, so an algorithm that keeps the distance matrix explicit needs about $n^2$ time per update on some sequences. The [Demetrescu-Italiano algorithm](/demetrescu-italiano-apsp/) reaches this bound up to logarithmic factors, amortized and deterministic, with $O(1)$ query time.

## In plain words

An airline keeps a table of the fastest connection between every pair of airports. Flights are added, removed, or change their duration. After each change, the table must be correct again.

One change can affect a large part of the table. If a flight is the only link between two halves of the network, removing it changes every entry from one half to the other. So some updates must touch about the whole table. The goal is to make each update cost about as much as writing the table once, and not as much as computing it from zero, which is many times slower.

## Definition

**Input.** A directed graph $G = (V, E)$ on $n$ vertices with weights $w : E \to \mathbb{R}_{\ge 0}$, and an online sequence of updates mixed with queries $\mathrm{dist}(x, y)$, which return the weight of a lightest path from $x$ to $y$, or $\infty$.

**Updates.**

- An **edge update** inserts or deletes an edge, or changes its weight.
- A **vertex update** changes, inserts or deletes any set of edges that all touch one vertex $v$. Demetrescu and Italiano use this stronger form.

**Kinds of updates.** Insertions and weight decreases give the **incremental** problem, deletions and increases the **decremental** problem, and both the **fully dynamic** problem. Each bound is worst case or [amortized](/amortized-update-time/), and deterministic or randomized.

**Path queries.** A stronger query returns a shortest path in time proportional to its number of edges.

## Variants

- **Fully dynamic, exact, real weights.** The main problem of this page.
- **Small integer weights.** Weights in $\{1, \ldots, C\}$, where bounds may depend on $C$.
- **Decremental or incremental.** Partially dynamic versions, often built from one [decremental SSSP](/decremental-sssp/) structure per source.
- **Approximate.** Keep distances within a factor $\alpha$, often in undirected graphs; these allow update times far below $n^2$.
- **Negative weights.** Allowed by some algorithms, which must then also report negative cycles.
- **Reachability only.** Keep only whether $d(x, y) < \infty$; see [dynamic transitive closure](/dynamic-transitive-closure/).

## Examples

Take two directed triangles, $0 \to 1 \to 2 \to 0$ and $3 \to 4 \to 5 \to 3$, with unit weights, joined by the edge $2 \to 3$ of weight 5. At the start $d(0, 3) = 7$, $d(0, 5) = 9$, and no vertex of $\{3, 4, 5\}$ reaches $\{0, 1, 2\}$.

| update | changed pairs | $d(0, 3)$ | $d(0, 4)$ | $d(3, 0)$ |
|---|---|---|---|---|
| set weight of $2 \to 3$ to 1 | 9 | 3 | 4 | ∞ |
| insert $1 \to 4$ (1) | 4 | 3 | 2 | ∞ |
| delete $2 \to 3$ | 5 | 4 | 2 | ∞ |
| delete $1 \to 4$ | 9 | ∞ | ∞ | ∞ |
| insert $5 \to 0$ (2) | 9 | ∞ | ∞ | 4 |

The first update changes all 9 distances from the first triangle to the second, because every such path uses the edge $2 \to 3$. With $n/2$ vertices on each side, the same construction changes $n^2/4$ distances, and alternating the last two updates repeats this as often as wanted. So an algorithm that keeps every distance in an explicit matrix needs $\Omega(n^2)$ amortized time per update for some sequences.

## Known algorithms

| algorithm | updates | update time | query | case | deterministic |
|---|---|---|---|---|---|
| recompute with Floyd-Warshall | any | $O(n^3)$ | $O(1)$ | worst | yes |
| one [Dijkstra](/dijkstra/) per source after each update | any | $O(mn + n^2 \log n)$ | $O(1)$ | worst | yes |
| King (1999), weights in $\{1, \ldots, C\}$ | edge | $O(n^{2.5} (C \log n)^{1/2})$ | $O(1)$ | amortized | yes |
| [Demetrescu and Italiano](/demetrescu-italiano-apsp/) (2004) | vertex | $O(n^2 \log^3 n)$ | $O(1)$ | amortized | yes |
| Thorup (2004) | vertex | $\tilde O(n^2)$, smaller polylog factor | $O(1)$ | amortized | yes |
| Thorup (2005) | vertex | $\tilde O(n^{2.75})$ | $O(1)$ | worst | yes |
| Abraham, Chechik and Krinninger (2017) | vertex | $\tilde O(n^{2 + 2/3})$ | $O(1)$ | worst | no, Monte Carlo |

**Locally shortest paths.** The Demetrescu-Italiano approach keeps, besides the shortest paths, all paths whose every proper subpath is shortest. After an update, new shortest paths can only be built from such paths, so the update needs to look at far fewer candidates than a full recomputation. To bound the work over a whole sequence, the algorithm also keeps paths that were shortest at some earlier time. The [algorithm page](/demetrescu-italiano-apsp/) gives the details.

**Worst-case bounds.** The amortized algorithms can spend much more than $n^2$ time on one update. Thorup (2005) and later work rebuild the structure in the background, and give bounds between $n^2$ and $n^3$ for every single update.

## Bounds

**Upper bounds.** $\tilde O(n^2)$ amortized per vertex update, deterministic, with constant query time.

**Lower bounds.** As in the example, an explicit distance matrix needs $\Omega(n^2)$ amortized time per update on some sequences, so the amortized bound is optimal up to polylogarithmic factors for such algorithms. An algorithm that answers queries in more than constant time could avoid this, and here conditional lower bounds from the [OMv conjecture](/omv-conjecture/) and from the hardness of static all-pairs shortest paths limit the trade-off between update and query time.

## Reductions

- **Static to dynamic.** Inserting the edges one at a time into an incremental structure computes static all-pairs shortest paths, so an incremental algorithm much faster than $n^3 / m$ amortized per insertion would beat the best known static algorithms on dense graphs.
- **Single source.** A dynamic APSP structure answers [dynamic single-source shortest paths](/dynamic-single-source-shortest-paths/) and [dynamic reachability](/dynamic-reachability/).
- **Vertex updates to edge updates.** A vertex update is a sequence of up to $2n$ edge updates, so a bound per vertex update is much stronger than the same bound per edge update.

## Applications

- **Routing tables.** Networks keep distances between all pairs of routers.
- **Road networks and transit.** Distance tables used by planners change with closures and delays.
- **Graph analysis.** Measures such as closeness centrality and the diameter of a changing graph use all distances.

## References
