---
tag: MYJZS3
kind: definition
slug: dynamic-graph
name: Dynamic graph
aliases:
- dynamic graph problem
area: graphs/dynamic-graphs
level: intro
summary: A graph whose edge or vertex set changes under a sequence of updates, with queries answered between them.
prereqs: [graph, connected-components]
see_also: [fully-dynamic-graph, incremental-graph, decremental-graph, offline-dynamic-graph, temporal-graph, amortized-update-time, worst-case-update-time, update-query-tradeoff]
sources:
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 1 (the fully dynamic, partially dynamic and insertions-only settings, and the update and query operations)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 1 (the fully dynamic model with edge insertions, edge deletions and queries)
  - url: https://arxiv.org/abs/2102.11169
    title: Kathrin Hanauer, Monika Henzinger and Christian Schulz, Recent advances in fully dynamic graph algorithms, a quick reference guide, ACM Journal of Experimental Algorithmics 27 (2022)
    locator: Section 1 (the terms fully dynamic, incremental, decremental, amortized and worst-case update time)
---

A dynamic graph is a [graph](/graph/) that changes over time through a sequence of updates, such as the insertion or deletion of an [edge](/edge/), while a program answers queries about its current state between the updates. A dynamic graph problem asks for a data structure that keeps some property of the graph, such as its [connected components](/connected-components/), up to date, so that each update and each query is much cheaper than a computation from scratch. The kinds of updates that the problem allows decide its difficulty: insertions only, deletions only, or both.

## Definition

Fix a vertex set $V$ with $n = |V|$. A **dynamic graph** is a sequence of graphs $G_0, G_1, G_2, \ldots$ on $V$, where $G_0$ is given at the start (often with no edges) and $G_i$ comes from $G_{i-1}$ by one **update**. The basic edge updates are

- $\mathrm{insert}(u, v)$: $E_i = E_{i-1} \cup \{\{u, v\}\}$, for an edge that is not in $E_{i-1}$,
- $\mathrm{delete}(u, v)$: $E_i = E_{i-1} \setminus \{\{u, v\}\}$, for an edge that is in $E_{i-1}$.

For a directed graph the pairs are ordered. For a weighted graph an update can also change the weight $w(u, v)$ of an edge that stays in the graph. A **vertex update** changes all edges at one vertex $v$ in one operation: it can insert a set of edges at $v$, delete a set of edges at $v$, or both.

A **dynamic graph problem** is given by a set of allowed updates and a query function $q$. After update $i$, a query with argument $x$ must return $q(G_i, x)$. For example, in [dynamic connectivity](/dynamic-connectivity/) the query $\mathrm{connected}(u, v)$ returns whether $u$ and $v$ are in the same component of $G_i$. An algorithm for the problem is a data structure with a preprocessing step for $G_0$, an update procedure and a query procedure.

The allowed updates give three classes:

- **Incremental** (insertions only): every update inserts an edge. See [incremental graph](/incremental-graph/).
- **Decremental** (deletions only): every update deletes an edge. See [decremental graph](/decremental-graph/).
- **Fully dynamic**: both insertions and deletions. See [fully dynamic graph](/fully-dynamic-graph/).

Incremental and decremental problems together are called **partially dynamic**.

The cost of an algorithm has three parts: the preprocessing time, the **update time** and the **query time**. A bound on the update time can be worst case for each update, [amortized](/amortized-update-time/) over any sequence, or expected over the random choices of a randomized algorithm. In the usual **online** setting, the algorithm learns each update or query only after it has answered the previous query. In the **offline** setting it knows the whole sequence in advance; see [offline dynamic graph](/offline-dynamic-graph/).

## Examples and non-examples

**Example: a fully dynamic sequence.** Take $V = \{0, 1, 2, 3, 4, 5\}$ and $G_0$ with no edges, so there are 6 components. The table shows the edge set and the number of components after each operation of a fully dynamic connectivity instance.

| step | operation | edges after it | components | answer |
|---|---|---|---|---|
| 1 | insert(0, 1) | 01 | 5 | |
| 2 | insert(1, 2) | 01, 12 | 4 | |
| 3 | insert(3, 4) | 01, 12, 34 | 3 | |
| 4 | connected(0, 2) | 01, 12, 34 | 3 | yes |
| 5 | delete(1, 2) | 01, 34 | 4 | |
| 6 | connected(0, 2) | 01, 34 | 4 | no |
| 7 | insert(2, 5) | 01, 25, 34 | 3 | |
| 8 | insert(5, 0) | 01, 25, 34, 05 | 2 | |
| 9 | connected(0, 2) | 01, 25, 34, 05 | 2 | yes |
| 10 | delete(0, 1) | 25, 34, 05 | 3 | |

The deletion at step 5 splits a component, and the insertion at step 8 joins two. The answer to the same query $\mathrm{connected}(0, 2)$ changes twice. A structure that only merges sets, such as a [disjoint-set forest](/disjoint-set-forest/), handles steps 1 to 4 but cannot undo the merge at step 5.

**Example: incremental.** Kruskal's algorithm grows a forest by edge insertions and asks, before each insertion, whether the two ends are already connected. This is incremental connectivity, and a [disjoint-set](/disjoint-set/) structure answers it in $O(\alpha(n))$ amortized time per operation, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/).

**Example: decremental.** Even and Shiloach (1981) keep the [breadth-first search](/breadth-first-search/) levels from a source while edges are deleted. This is a decremental problem; see the [Even-Shiloach tree](/even-shiloach-tree/).

**Non-example: a static graph with many queries.** If the graph never changes, one computation answers all queries. For connectivity, one [depth-first search](/depth-first-search/) labels the components in $O(n + m)$ time and each later query takes $O(1)$ time. The dynamic setting starts only when updates and queries interleave.

**Non-example: a stream with one pass.** In the streaming model the edges also arrive one at a time, but the main limit is memory, often $O(n \operatorname{polylog} n)$ words, and the answer is often needed only at the end. A dynamic graph algorithm may store the whole graph, and it must answer queries at any time.

**Non-example: a temporal graph.** A [temporal graph](/temporal-graph/) gives each edge the time interval in which it exists, and its queries can ask about paths that respect time. The whole history is the input. A dynamic graph algorithm sees only the present graph and must answer about it.

## Related definitions

- **[Fully dynamic graph](/fully-dynamic-graph/), [incremental graph](/incremental-graph/) and [decremental graph](/decremental-graph/)** are the three classes above.
- **[Offline dynamic graph](/offline-dynamic-graph/).** The whole sequence of updates and queries is known in advance. Divide and conquer over time and the [rollback technique](/rollback-technique/) then often give simple and fast algorithms.
- **[Amortized update time](/amortized-update-time/) and [worst-case update time](/worst-case-update-time/)** are the two usual cost measures of an update.
- **[Update and query trade-off](/update-query-tradeoff/).** A structure can make updates cheap and queries expensive, or the reverse. Lower bounds are often stated as a bound on the larger of the two, or on their product.
- **Dynamic tree.** When the graph is a forest at all times, the problem is a [dynamic tree](/dynamic-tree/) problem, and [link-cut trees](/link-cut-tree/) and [Euler tour trees](/euler-tour-tree/) solve it in $O(\log n)$ time per operation.
- **Adversary.** For a randomized algorithm, an [oblivious adversary](/oblivious-adversary/) fixes the whole sequence before the algorithm runs, and an [adaptive adversary](/adaptive-adversary/) may choose the next update after it sees the earlier answers. A bound against an oblivious adversary need not hold against an adaptive one.

## References
