---
tag: 6SA9G8
kind: concept
slug: worst-case-update-time
name: Worst-case update time
aliases:
- worst-case update cost
- de-amortized update time
area: graphs/dynamic-graphs
level: core
summary: Maximum cost of any single update, stronger than amortized update time.
prereqs: [dynamic-graph, amortized-update-time]
see_also: [amortized-vs-worst-case, global-rebuilding, sparsification, frederickson-topology-trees, blum-union-find, update-query-tradeoff, rollback-technique, euler-tour-tree]
sources:
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 1 and the results on minimum spanning forests and connectivity (O(n^(1/2)) worst-case time per update)
  - paper: doi:10.1137/0214055
    title: Greg N. Frederickson, Data structures for on-line updating of minimum spanning trees, with applications, SIAM Journal on Computing 14(4), 781 to 798 (1985)
    locator: the main result (O(m^(1/2)) worst-case time per update for minimum spanning trees)
  - paper: doi:10.1137/1.9781611973105.81
    title: Bruce M. Kapron, Valerie King and Ben Mountjoy, Dynamic graph connectivity in polylogarithmic worst case time, Proceedings of SODA 2013, 1131 to 1142
    locator: Section 1 (worst-case against amortized bounds) and the main theorem
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345 to 354
    locator: Theorem 6 (the worst-case lower bound per operation for union-find)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 16, Amortized Analysis (Section 16.4, dynamic tables, for the amortized bound that the example de-amortizes)
---

The worst-case update time of a [dynamic graph](/dynamic-graph/) algorithm is a bound $T$ such that every single update, in every sequence of updates, takes at most $T$ time. It is stronger than the [amortized update time](/amortized-update-time/), which bounds only the average over a sequence and allows a rare update to be very slow. Real-time systems, interactive programs and algorithms that undo operations need worst-case bounds. For several problems the best worst-case bounds are much larger than the best amortized ones, so the difference is not a technicality.

## In plain words

An amortized promise says: over the whole run, changes cost little on average. A worst-case promise says: no single change ever costs more than this. The second promise is stronger, because an average can hide one very slow step.

The difference matters when someone waits for each step. A game must draw every frame on time, and a router must handle every packet on time. One slow step is a visible failure, even if the average is fine.

To turn an average promise into a per-step promise, a program spreads its big clean-up jobs into small pieces and does one piece at each change, so that no single change has to do the whole job.

## The idea

**Definition.** Let a dynamic algorithm start from the graph $G_0$ after preprocessing. It has **worst-case update time** $T(n, m)$ if for every sequence of allowed updates and for every $i$,

$$t_i \le T(n, m),$$

where $t_i$ is the time of the $i$-th update, $n$ is the number of vertices and $m$ is the current (or largest) number of edges. Worst-case query time is defined in the same way. A worst-case bound implies the same amortized bound, since $\sum_{i=1}^{k} t_i \le kT$. The reverse is false: an amortized bound of $O(1)$ allows one update of cost $\Theta(k)$ after $k$ cheap ones.

**Randomized algorithms.** For a randomized algorithm, "worst-case expected" means $\mathbb{E}[t_i] \le T$ for each $i$, and "worst case with high probability" means $\Pr[t_i > T] \le n^{-c}$ for each $i$, for a constant $c$. Both are per update, not per sequence. The bound may assume an [oblivious adversary](/oblivious-adversary/).

**Deamortization.** An amortized algorithm usually pays for a rare expensive step, such as a rebuild, with many cheap steps before it. To make the bound worst case, the algorithm starts the expensive step early and does a constant share of it at each later update, while it keeps serving queries from the old copy. When the new copy is ready, it switches. This is [global rebuilding](/global-rebuilding/). It needs two copies of the structure and a way to replay the updates that arrive during the rebuild.

**Why some gaps cannot be closed.** Deamortization is not always possible at the same cost. For [incremental connectivity](/incremental-connectivity/) (union-find), the amortized cost per operation is $\Theta(\alpha(n))$, but Fredman and Saks (1989) proved that the worst case per operation is $\Theta(\log n / \log\log n)$ in the cell-probe model, matched by [Blum's structure](/blum-union-find/). So for this problem the worst-case bound is provably larger by a factor that grows without bound.

## Examples

**A dynamic array.** With doubling, a push into a full array of capacity $c$ copies $c$ items. For 17 pushes from capacity 1, the costs in writes are

$$1, 2, 3, 1, 5, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 17,$$

which sum to 48, under 3 per push on average, while the last push alone costs 17. To make each push cost $O(1)$, allocate the new array of capacity $2c$ as soon as the old one is full, and at each later push, write the new item into the new array and copy 2 old items. After $c/2$ pushes all $c$ old items are copied, while the new array holds only $1.5c$ items, so the copy ends before the new array fills up. Each push then does at most 3 writes, in the worst case, assuming allocation without initialization takes $O(1)$ time.

**Fully dynamic connectivity and minimum spanning forests.** Frederickson (1985) gave $O(m^{1/2})$ worst-case time per update for minimum spanning trees with [topology trees](/frederickson-topology-trees/). [Sparsification](/sparsification/) by Eppstein, Galil, Italiano and Nissenzweig (1997) lowered this to $O(n^{1/2})$ worst case, deterministically. The [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/) of 2001 reaches $O(\log^2 n)$ for connectivity, but only amortized. Kapron, King and Mountjoy (2013) gave the first polylogarithmic worst-case bound, with a randomized Monte Carlo algorithm. So for more than a decade the worst-case bound and the amortized bound of this problem were far apart.

**Dynamic trees.** An [Euler tour tree](/euler-tour-tree/) stored in a balanced search tree such as a red-black tree takes $O(\log n)$ worst-case time per link and cut. A [link-cut tree](/link-cut-tree/) on [splay trees](/splay-tree/) takes $O(\log n)$ amortized time, and a single operation can take $\Theta(n)$ time. Top trees built on [topology trees](/frederickson-topology-trees/) give $O(\log n)$ in the worst case.

**Undo.** A structure with an undo operation must use worst-case bounds, because an adversary can repeat "do the expensive update, undo it". The [rollback technique](/rollback-technique/) and [union-find with rollback](/union-find-with-rollback/) rely on this.

## Where it is used

- **Real-time and interactive systems**, where each update has a deadline: network routing tables, game engines, user interfaces.
- **Subroutines that undo**, such as [offline dynamic connectivity](/offline-dynamic-connectivity/), which applies and undoes edges in a recursion over time.
- **Parallel and distributed settings**, where one slow update blocks all processors that wait for it.
- **Stating results.** A table of dynamic graph results must mark each bound as worst case, amortized or expected. See [amortized update time](/amortized-update-time/) and the [update and query trade-off](/update-query-tradeoff/) for the other measures.
- **Deamortization techniques**: [global rebuilding](/global-rebuilding/), [lazy rebuilding](/lazy-rebuilding/), and the background copying of the dynamic array example.

## References
