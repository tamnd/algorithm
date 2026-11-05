---
tag: DM6REV
kind: problem
slug: dynamic-minimum-cut
name: Dynamic minimum cut
aliases:
- fully dynamic minimum cut
- dynamic edge connectivity
area: graphs/dynamic-graphs
level: research
summary: Maintain the value of a minimum cut under edge insertions and deletions.
prereqs: [dynamic-graph, global-min-cut-problem, edge-connectivity, dynamic-connectivity]
see_also: [stoer-wagner, karger-min-cut, gomory-hu-tree, dynamic-biconnectivity, sparsification, min-cut-problem, omv-conjecture]
sources:
  - paper: doi:10.1007/s00493-007-0045-2
    title: Mikkel Thorup, Fully-dynamic min-cut, Combinatorica 27(1), 91 to 127 (2007)
    locator: the main theorems (exact minimum cuts of polylogarithmic size, and a (1 + o(1))-approximation in general, in O~(n^(1/2)) worst-case time per update)
  - paper: doi:10.1145/3174803
    title: Gramoz Goranci, Monika Henzinger and Mikkel Thorup, Incremental exact min-cut in polylogarithmic amortized update time, ACM Transactions on Algorithms 14(2), 1 to 21 (2018)
    locator: the main theorem (deterministic, O(log^3 n (log log n)^2) amortized time per insertion, O(1) query time)
  - paper: doi:10.1137/1.9781611977554.ch3
    title: Gramoz Goranci, Monika Henzinger, Danupon Nanongkai, Thatchaphol Saranurak, Mikkel Thorup and Christian Wulff-Nilsen, Fully dynamic exact edge connectivity in sublinear time, Proceedings of SODA 2023, 70 to 86
    locator: the two main theorems (O~(n) worst-case and O~(m^(1 - 1/31)) amortized update time for simple graphs)
  - paper: doi:10.1137/1.9781611977912.107
    title: Wenyu Jin, Xiaorui Sun and Mikkel Thorup, Fully dynamic min-cut of superconstant size in subpolynomial time, Proceedings of SODA 2024, 2999 to 3026
    locator: the main theorem
  - paper: doi:10.1145/2746539.2746609
    title: Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, Proceedings of STOC 2015, 21 to 30
    locator: the table of results (conditional lower bounds for dynamic problems, including weighted minimum cut)
---

The dynamic minimum cut problem asks to keep the [edge connectivity](/edge-connectivity/) $\lambda(G)$ of an undirected [dynamic graph](/dynamic-graph/), the smallest number of edges whose removal disconnects it, while edges are inserted and deleted. The static problem is the [global minimum cut](/global-min-cut-problem/) problem. When $\lambda$ is small, or with insertions only, polylogarithmic or subpolynomial update times are known. For the exact fully dynamic problem with no bound on $\lambda$, the first sublinear update time for simple graphs came only in 2023.

## In plain words

A network is as strong as its weakest cut: the smallest set of links that, once cut, splits the network into two parts. The task is to know the size of that weakest cut while links are added and removed.

A new link can only make the network stronger, and a lost link can only make it weaker, by at most one. The weak spot is often a single node with few links, but it can also be a thin bridge between two big groups, and these are hard to find. Fast methods keep a small summary of the network that has the same weak spots, and repair only that summary.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices, simple or with parallel edges and weights, and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates.

**Output.** After each update, the value $\lambda(G) = \min_{\emptyset \ne S \subsetneq V} |\delta(S)|$, where $\delta(S)$ is the set of edges with exactly one end in $S$. A stronger query returns a set $S$ that attains it. An $\alpha$-approximate structure returns a value between $\lambda(G)$ and $\alpha \lambda(G)$.

**Cost.** Update time, worst case or [amortized](/amortized-update-time/), and query time. Updates are insertions only, deletions only, or both.

**Basic facts.** For an unweighted graph, one insertion raises $\lambda$ by at most 1 and one deletion lowers it by at most 1. $\lambda(G) \le \delta_{\min}(G)$, the minimum degree, since a single vertex is a side of a cut. The graph is connected exactly when $\lambda \ge 1$, so [dynamic connectivity](/dynamic-connectivity/) is the question "$\lambda \ge 1$?".

## Variants

- **Insertions only.** $\lambda$ only grows.
- **Fully dynamic, bounded $\lambda$.** Exact answers when $\lambda$ is at most some bound $k$; for $k = 1$ and $k = 2$ this is connectivity and [2-edge connectivity](/dynamic-biconnectivity/).
- **Approximate.** A factor $1 + \varepsilon$ or $2$.
- **Weighted.** Edge weights, with weight updates.
- **$s$-$t$ minimum cut.** Keep the [minimum $s$-$t$ cut](/min-cut-problem/) for fixed $s$ and $t$, which is a maximum flow value.
- **All pairs.** Keep a [Gomory-Hu tree](/gomory-hu-tree/), which gives every $s$-$t$ minimum cut value.

## Examples

Take two triangles $0, 1, 2$ and $3, 4, 5$ joined by the edge $23$. The table gives $\lambda$, a minimum cut, and the minimum degree after each update.

| update | $\lambda$ | a minimum cut | minimum degree |
|---|---|---|---|
| start | 1 | $\{0, 1, 2\}$, edge 23 | 2 |
| insert 04 | 2 | $\{0, 1, 2\}$, edges 23, 04 | 2 |
| insert 15 | 3 | $\{0, 1, 2\}$, edges 23, 04, 15 | 3 |
| delete 23 | 2 | $\{0, 1, 2\}$, edges 04, 15 | 2 |
| insert 03 | 2 | $\{2\}$, edges 12, 20 | 2 |
| insert 14 | 2 | $\{2\}$, edges 12, 20 | 2 |
| delete 01 | 2 | $\{2\}$, edges 12, 20 | 2 |

In the first four rows the cut between the two triangles is a minimum cut. In the first row it is smaller than every vertex degree, so looking at degrees alone gives the wrong answer; in the next three rows it ties with the minimum degree. From the fifth row on, vertex $2$, whose links to the other side were removed, is a minimum cut by itself.

## Known algorithms

**Static.** [Stoer-Wagner](/stoer-wagner/) runs in $O(m n + n^2 \log n)$ time, [Karger's](/karger-min-cut/) near-linear randomized algorithms in $O(m \log^3 n)$, and deterministic near-linear algorithms exist for simple graphs. Recomputing after each update costs this much.

| setting | algorithm | update time | case |
|---|---|---|---|
| any | recompute | near-linear in $m$ | worst |
| insertions only, exact | Goranci, Henzinger and Thorup (2016, 2018) | $O(\log^3 n (\log\log n)^2)$ | amortized, deterministic |
| fully dynamic, $\lambda$ up to polylog, exact | Thorup (2001, 2007) | $\tilde O(n^{1/2})$ | worst |
| fully dynamic, $1 + o(1)$ approximation | Thorup (2001, 2007) | $\tilde O(n^{1/2})$ | worst |
| fully dynamic, exact, simple graphs | Goranci et al. (2023) | $\tilde O(n)$ | worst |
| fully dynamic, exact, simple graphs | Goranci et al. (2023) | $\tilde O(m^{1 - 1/31})$ | amortized |
| fully dynamic, $\lambda$ superconstant but small, exact | Jin, Sun and Thorup (2024) | $n^{o(1)}$ | worst |

**Insertions only.** Goranci, Henzinger and Thorup combine a sparsification for simple graphs, which contracts the graph to $O(m/\delta_{\min})$ edges while it keeps every non-trivial minimum cut, with an exact incremental algorithm of Henzinger (1997). The incremental algorithm keeps all minimum cuts in a cactus and discards those that an insertion crosses; when none is left, $\lambda$ has grown by 1 and the cuts are rebuilt. In a simple graph $\lambda \le n - 1$, so $\lambda$ grows at most $n - 1$ times, and the rebuilds are paid for.

**Thorup's tree packing.** A greedy packing of spanning trees has, for each minimum cut, a tree that crosses it at most twice. Thorup keeps such a packing dynamically, and for each tree keeps the cuts that cross it once or twice with [dynamic tree](/dynamic-tree/) structures. This gives exact answers while $\lambda$ is polylogarithmic. For a large $\lambda$, random sampling of edges with probability about $\log n / (\varepsilon^2 \lambda)$ keeps all cut values within $1 \pm \varepsilon$ after scaling, and lowers $\lambda$ to $O(\log n / \varepsilon^2)$.

## Bounds

**Upper bounds.** As in the table.

**Lower bounds.** Dynamic connectivity is the case $k = 1$, so the $\Omega(\log n)$ cell-probe bound of the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/) holds for "is $\lambda \ge 1$?". Goranci, Henzinger and Thorup point out a polynomial conditional lower bound for the fully dynamic weighted minimum cut problem, which comes from the [OMv](/omv-conjecture/) framework of Henzinger, Krinninger, Nanongkai and Saranurak (2015). So the exact weighted fully dynamic problem is not expected to have polylogarithmic update time, in contrast with the incremental problem.

## Reductions

- **From connectivity.** $G$ is connected exactly when $\lambda(G) \ge 1$.
- **From 2-edge connectivity.** $\lambda(G) \ge 2$ exactly when $G$ is connected and has no bridge.
- **To $s$-$t$ cuts.** $\lambda(G) = \min_{t \ne s} \lambda(s, t)$ for any fixed $s$, so $n - 1$ dynamic $s$-$t$ cut structures give $\lambda$.
- **Sampling.** For a $(1 + \varepsilon)$-approximation, sampled subgraphs with small $\lambda$ reduce the general problem to the bounded one.

## Applications

- **Network reliability.** The edge connectivity is the number of link failures a network survives, and it changes as links are added and removed.
- **Graph clustering.** Minimum cuts split a graph into well-connected parts, and dynamic versions keep the split of a changing graph.
- **Subroutine.** Dynamic expander decompositions and cut sparsifiers use minimum cut values of parts of the graph.

## References
