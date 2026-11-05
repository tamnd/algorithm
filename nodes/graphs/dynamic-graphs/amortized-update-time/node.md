---
tag: NXSGF8
kind: concept
slug: amortized-update-time
name: Amortized update time
aliases:
- amortized update cost
area: graphs/dynamic-graphs
level: core
summary: Average cost per update over a sequence, the usual measure for dynamic graph algorithms.
prereqs: [dynamic-graph, amortized-cost, potential-method]
see_also: [worst-case-update-time, update-query-tradeoff, decremental-graph, dynamic-connectivity, union-by-size, global-rebuilding, lazy-rebuilding]
sources:
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 306 to 318 (1985)
    locator: Sections 1 and 2 (the definition of amortized time and the potential argument)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 16, Amortized Analysis (aggregate analysis, the accounting method and the potential method)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 1 and the main theorem on connectivity (amortized update time and worst-case query time)
  - paper: doi:10.1137/1.9781611973105.81
    title: Bruce M. Kapron, Valerie King and Ben Mountjoy, Dynamic graph connectivity in polylogarithmic worst case time, Proceedings of SODA 2013, 1131 to 1142
    locator: Section 1 (amortized against worst-case bounds for dynamic connectivity)
---

The amortized update time of a [dynamic graph](/dynamic-graph/) algorithm is a bound $T$ such that, for every sequence of $k$ updates from the start, the total time of the updates is at most $k \cdot T$. It is an [amortized cost](/amortized-cost/): a single update may take much longer than $T$, but expensive updates must be rare enough that the average over any sequence stays below $T$. Most of the classic bounds for fully dynamic graph problems, such as the $O(\log^2 n)$ bound for [dynamic connectivity](/dynamic-connectivity/), are amortized. The stronger measure, a bound on every single update, is the [worst-case update time](/worst-case-update-time/).

## In plain words

A program keeps an answer about a graph up to date while edges come and go. Most changes are cheap to handle, but now and then a change forces a big clean-up. The amortized update time is the cost of one change on average over the whole run, in the worst run that anyone can build.

It is not an average over random inputs. The promise holds for every sequence of changes, even one chosen by an enemy. What it does not promise is that each single change is fast. A program that must answer within a fixed delay after every change, such as a network router, needs the stronger worst-case promise. A program that only cares about the total running time, such as a batch job, can use the amortized one.

## The idea

**Definition.** Let a dynamic algorithm start from the graph $G_0$ after a preprocessing step. It has **amortized update time** $T(n, m)$ if for every $k \ge 1$ and every sequence of $k$ allowed updates,

$$\sum_{i=1}^{k} t_i \le k \cdot T(n, m),$$

where $t_i$ is the time of update $i$, $n$ is the number of vertices and $m$ is the largest number of edges during the sequence. Amortized query time is defined in the same way. When updates and queries mix, the condition is on the total time of any prefix of operations: it is at most the sum of the amortized bounds of the operations in that prefix. The worst-case bound $\max_i t_i \le T$ implies the amortized bound, and the reverse is false.

**Total update time.** For a [decremental graph](/decremental-graph/) or an incremental graph the number of updates is at most $m$, so the cost is often given as a total over the whole sequence. A total of $O(mn)$ over $m$ deletions is $O(n)$ amortized per deletion.

**How the bounds are proved.** The tools are those of amortized analysis. The [aggregate method](/aggregate-method/) bounds the total cost directly. The [potential method](/potential-method/) defines a potential $\Phi \ge 0$ of the state, with $\Phi_0 = 0$, and shows $t_i + \Phi_i - \Phi_{i-1} \le T$ for each update $i$. Summing over $i$ gives $\sum t_i \le kT - \Phi_k \le kT$. In dynamic graph algorithms the potential is often a count of levels: each edge or vertex has a level that only moves in one direction and is bounded, so the total number of moves is bounded.

**Expected and amortized.** A randomized algorithm can have an expected amortized bound: the expected total time of any fixed sequence of $k$ updates is at most $kT$. This bound is usually proved against an [oblivious adversary](/oblivious-adversary/), which fixes the sequence before the run. Against an [adaptive adversary](/adaptive-adversary/), which sees the answers, it may fail.

**Why amortized bounds break.** Three common uses break the averaging.

- **Undo.** If the structure supports undoing the last update, an adversary can repeat "do the expensive update, undo it" forever. Each repetition costs the full price, so the average is no longer $T$. This is why the [rollback technique](/rollback-technique/) needs worst-case bounds, as with [union by size](/union-by-size/) without path compression.
- **Persistence and sharing.** If many versions of the structure are kept, an expensive step can be replayed on each version.
- **Real time.** A system with a deadline per update must meet $\max_i t_i$, not the average.

Turning an amortized bound into a worst-case bound is called deamortization. Spreading a rebuild over many later updates, as in [global rebuilding](/global-rebuilding/) and [lazy rebuilding](/lazy-rebuilding/), is the standard tool when the expensive step is a rebuild.

## Examples

**Relabel the smaller part.** Keep incremental connectivity with an array $\mathrm{label}[v]$ and a member list for each component. To insert an edge between two components, relabel every vertex of the smaller one. A single insertion can relabel $n/2$ vertices. But a vertex is relabeled only when its component at least doubles in size, so each vertex is relabeled at most $\lfloor \log_2 n \rfloor$ times, and $n - 1$ joining insertions cost at most $n \log_2 n$ relabels in total. This is $O(\log n)$ amortized per insertion and $\Theta(n)$ in the worst case. For $n = 16$, joining pairs, then pairs of pairs, and so on, takes 15 insertions:

| round | insertions | relabels each | total |
|---|---|---|---|
| 1 | 8 | 1 | 8 |
| 2 | 4 | 2 | 8 |
| 3 | 2 | 4 | 8 |
| 4 | 1 | 8 | 8 |

The total is 32, so the average is $32/15 \approx 2.13$ relabels per insertion, while the last insertion alone relabels 8 vertices.

**Fully dynamic connectivity.** Holm, de Lichtenberg and Thorup (2001) maintain connectivity under edge insertions and deletions in $O(\log^2 n)$ amortized time per update, deterministically, with $O(\log n / \log\log n)$ worst-case time per query. Each edge has a level that only goes up, and the potential argument charges the work of a deletion to these level increases. For worst-case bounds the history is different. Frederickson (1985) and then the sparsification of Eppstein, Galil, Italiano and Nissenzweig (1997) give $O(n^{1/2})$ worst case per update, deterministically. Kapron, King and Mountjoy (2013) give a polylogarithmic worst-case bound with a Monte Carlo algorithm.

**Decremental shortest paths.** The [Even-Shiloach tree](/even-shiloach-tree/) keeps breadth-first levels from one source under edge deletions in $O(mn)$ total time, because each vertex level only grows and is at most $n$. This is $O(n)$ amortized per deletion, while one deletion can take $\Theta(m)$ time.

**All-pairs shortest paths.** The [Demetrescu-Italiano algorithm](/demetrescu-italiano-apsp/) updates all distances of a directed graph after a vertex update in $O(n^2 \log^3 n)$ amortized time. Its analysis needs the amortization: the number of paths that one update changes can be far above the average.

## Where it is used

- **Stating dynamic graph results.** Most upper bounds for fully dynamic connectivity, minimum spanning forests, 2-edge and biconnectivity, and all-pairs shortest paths are amortized. A results table must say which bounds are amortized, which are worst case and which are expected.
- **Batch computations.** An algorithm that calls a dynamic structure as a subroutine, such as a static graph algorithm that deletes edges as it goes, needs only the total time, so an amortized bound gives the same running time as a worst-case one.
- **Lower bounds.** Cell-probe lower bounds for dynamic problems, such as those on the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/) page, hold for amortized time. So an amortized upper bound that matches them is optimal.
- **Choosing a structure.** For interactive or real-time use, prefer a worst-case bound; see [worst-case update time](/worst-case-update-time/) and the [update and query trade-off](/update-query-tradeoff/).

## References
