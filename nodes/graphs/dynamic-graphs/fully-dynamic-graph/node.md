---
tag: 8NJHAA
kind: definition
slug: fully-dynamic-graph
name: Fully dynamic graph
aliases:
- fully dynamic model
area: graphs/dynamic-graphs
level: intro
summary: Both edge insertions and edge deletions are allowed.
prereqs: [dynamic-graph]
see_also: [incremental-graph, decremental-graph, offline-dynamic-graph, dynamic-connectivity, holm-de-lichtenberg-thorup, amortized-update-time, worst-case-update-time, dynamic-connectivity-lower-bound]
sources:
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 1 (fully dynamic against partially dynamic problems)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 1 (the fully dynamic model) and the main theorems
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Pătraşcu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: the lower bound for fully dynamic connectivity
  - url: https://arxiv.org/abs/2102.11169
    title: Kathrin Hanauer, Monika Henzinger and Christian Schulz, Recent advances in fully dynamic graph algorithms, a quick reference guide, ACM Journal of Experimental Algorithmics 27 (2022)
    locator: Section 1 (terms) and the problem sections (tables of known bounds)
---

A fully dynamic graph is a [dynamic graph](/dynamic-graph/) whose updates may both insert and delete [edges](/edge/), in any order, for as long as the sequence runs. It is the most general of the three update classes: an algorithm for the fully dynamic setting also handles the [incremental](/incremental-graph/) and the [decremental](/decremental-graph/) settings, but the reverse is false. Without a direction of change, the counting arguments that bound the total work of partially dynamic algorithms stop working, so fully dynamic problems are usually the hardest.

## Definition

Fix a vertex set $V$ with $n = |V|$. A **fully dynamic graph** is a sequence of graphs $G_0, G_1, G_2, \ldots$ on $V$ in which each update $G_{i-1} \to G_i$ is one of

- $\mathrm{insert}(u, v)$ with $\{u, v\} \notin E_{i-1}$, so that $E_i = E_{i-1} \cup \{\{u, v\}\}$,
- $\mathrm{delete}(u, v)$ with $\{u, v\} \in E_{i-1}$, so that $E_i = E_{i-1} \setminus \{\{u, v\}\}$.

For directed graphs the pairs are ordered. For weighted graphs, an update may also set the weight $w(u, v)$ of a present edge to any new value, larger or smaller. In some problems a **vertex update** inserts or deletes a set of edges at one vertex in one step.

Three points separate this class from the partially dynamic ones.

- **No bound on the length.** An incremental sequence has at most $\binom{n}{2}$ updates, and a decremental one at most $m = |E_0|$. A fully dynamic sequence can be arbitrarily long, because the same edge can be inserted and deleted again and again. So costs are given per update (amortized, worst case or expected), not as a total.
- **The edge count changes.** The number of edges $m_i = |E_i|$ goes up and down. A bound in terms of $m$ usually means the current $m_i$ or the maximum over the sequence; a paper must say which.
- **No monotone quantity.** In a partially dynamic graph, distances, reachability and the component partition each move in one direction. In a fully dynamic graph they can move back and forth.

A **fully dynamic problem** fixes these updates and a query, such as $\mathrm{connected}(u, v)$, that must be answered for the current graph $G_i$.

## Examples and non-examples

**Example: a toggled edge.** Take a path $0, 1, \ldots, n-1$ and repeat $\mathrm{insert}(0, n-1)$, $\mathrm{delete}(0, n-1)$. For $n = 6$ the [breadth-first search](/breadth-first-search/) distances from 0 alternate between the two rows of the table.

| graph | distances from 0 to 0, 1, 2, 3, 4, 5 |
|---|---|
| path | 0, 1, 2, 3, 4, 5 |
| path plus edge 05 | 0, 1, 2, 3, 2, 1 |

Two distances change at each update. In general the vertices $v > n/2$ change, which is $\lceil n/2 \rceil - 1$ vertices, so for $n = 10$ four distances change at each update. An algorithm that stores all distances from 0 must rewrite $\Theta(n)$ values per update, for every update of an unbounded sequence. In a decremental graph each of these distances could grow at most $n$ times in total, which is what bounds the [Even-Shiloach tree](/even-shiloach-tree/) by $O(mn)$ total time; here no such total exists.

**Example: fully dynamic connectivity.** Insertions join components and deletions can split them. The [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/) handles both in $O(\log^2 n)$ amortized time per update, deterministically, and answers $\mathrm{connected}(u, v)$ in $O(\log n / \log\log n)$ time. Pătraşcu and Demaine proved that every structure in the cell-probe model needs $\Omega(\log n)$ amortized time per operation for this problem; see the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/). For forests, where each insertion joins two trees, a [link-cut tree](/link-cut-tree/) or an [Euler tour tree](/euler-tour-tree/) takes $O(\log n)$ time per operation.

**Example: the toggling adversary.** Let a structure have a cheap amortized bound only because its expensive steps are rare. In a fully dynamic setting an adversary can often find one update whose handling is expensive and its inverse, and repeat the pair. This is why fully dynamic algorithms need an argument that holds for every sequence, such as the edge levels of the Holm-de Lichtenberg-Thorup algorithm, whose potential still works when an edge comes back.

**Non-example: insertions only.** The sequence insert$(0, 1)$, insert$(1, 2)$, insert$(2, 3)$ is a valid fully dynamic sequence, but a sequence that can contain only insertions is the [incremental graph](/incremental-graph/) class. Its problems often have much faster algorithms: incremental connectivity takes $O(\alpha(n))$ amortized time per operation with a [disjoint-set forest](/disjoint-set-forest/).

**Non-example: a known sequence.** If the whole update sequence is given before the first query must be answered, the setting is the [offline dynamic graph](/offline-dynamic-graph/), even when the sequence has both insertions and deletions. Offline connectivity has a simple solution in $O(\log^2 n)$ time per operation by [divide and conquer over time](/offline-dynamic-connectivity/), which needs no fully dynamic structure.

**Non-example: weight decreases only.** A weighted sequence that only lowers weights (or inserts edges) is incremental for shortest paths, because distances only go down.

## Related definitions

- **[Incremental graph](/incremental-graph/) and [decremental graph](/decremental-graph/).** The two partially dynamic classes. A fully dynamic algorithm solves both, with the same bounds.
- **From partially dynamic to fully dynamic.** A common method keeps a decremental structure and rebuilds it from scratch after a fixed number of insertions, handling the recent insertions separately. The cost of the rebuild is spread over those insertions, so the bound is amortized unless the rebuild is spread out in time.
- **[Amortized update time](/amortized-update-time/) and [worst-case update time](/worst-case-update-time/).** For fully dynamic connectivity, the best deterministic amortized bound is polylogarithmic, while for decades the best deterministic worst-case bound was $O(n^{1/2})$ by [sparsification](/sparsification/).
- **[Update and query trade-off](/update-query-tradeoff/).** Lower bounds for fully dynamic problems are often stated for the larger of the update time and the query time.
- **Adversary.** For a randomized fully dynamic algorithm, the bound may assume an [oblivious adversary](/oblivious-adversary/). An [adaptive adversary](/adaptive-adversary/) can use the answers to pick the next insertion or deletion.

## References
