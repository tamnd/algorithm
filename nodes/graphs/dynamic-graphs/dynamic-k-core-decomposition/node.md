---
tag: X7RT7W
kind: problem
slug: dynamic-k-core-decomposition
name: Dynamic k-core decomposition
aliases:
- dynamic core decomposition
- core maintenance
area: graphs/dynamic-graphs
level: research
summary: Maintain the core number of every vertex under edge updates.
prereqs: [dynamic-graph, k-core, k-core-decomposition, degeneracy]
see_also: [dynamic-densest-subgraph, arboricity, amortized-update-time, dynamic-graph-coloring, incremental-graph, decremental-graph]
sources:
  - paper: doi:10.14778/2536336.2536344
    title: Ahmet Erdem Sarıyüce, Buğra Gedik, Gabriela Jacques-Silva, Kun-Lung Wu and Ümit V. Çatalyürek, Streaming algorithms for k-core decomposition, Proceedings of the VLDB Endowment 6(6), 433 to 444 (2013)
    locator: the theorems on which vertices change their core number after one insertion or deletion, and the traversal algorithm
  - paper: doi:10.1109/tkde.2013.158
    title: Rong-Hua Li, Jeffrey Xu Yu and Rui Mao, Efficient core maintenance in large dynamic graphs, IEEE Transactions on Knowledge and Data Engineering 26(10), 2453 to 2465 (2014)
    locator: the results that core numbers change by at most 1 per edge update, and the color-based maintenance algorithms
  - paper: doi:10.1109/icde.2017.93
    title: Yikai Zhang, Jeffrey Xu Yu, Ying Zhang and Lu Qin, A fast order-based approach for core maintenance, Proceedings of ICDE 2017, 337 to 348
    locator: the order-based insertion and deletion algorithms
  - paper: doi:10.1145/3385416
    title: Bintao Sun, T.-H. Hubert Chan and Mauro Sozio, Fully dynamic approximate k-core decomposition in hypergraphs, ACM Transactions on Knowledge Discovery from Data 14(4), 1 to 21 (2020)
    locator: the insertions-only and fully dynamic algorithms with polylogarithmic update time
  - paper: doi:10.1145/3490148.3538569
    title: Quanquan C. Liu, Jessica Shi, Shangdi Yu, Laxman Dhulipala and Julian Shun, Parallel batch-dynamic algorithms for k-core decomposition and related graph problems, Proceedings of SPAA 2022, 191 to 204
    locator: the level data structure and the approximate batch-dynamic core numbers
---

The dynamic $k$-core decomposition problem asks to keep the core number of every vertex of an undirected [dynamic graph](/dynamic-graph/) under edge insertions and deletions. The core number of $v$ is the largest $k$ such that $v$ lies in the [$k$-core](/k-core/), the largest subgraph in which every vertex has degree at least $k$. One edge update changes each core number by at most 1, and only near the updated edge in a precise sense, but it can still change $\Theta(n)$ core numbers. So exact algorithms are fast in practice but not in the worst case, and the algorithms with provable polylogarithmic bounds keep approximate core numbers.

## In plain words

Peel a network like an onion. First remove everyone with fewer than one friend, then everyone with fewer than two friends among those left, and so on. A person's core number is the layer at which they are peeled away. Highly connected groups sit deep in the onion.

When a friendship starts or ends, the layers move a little. Each person moves by at most one layer, and only people at the same layer as the new friendship can move. But a whole ring of people can drop together when one link of the ring breaks. Fast methods search only among the people who could move, and very fast methods allow the layers to be slightly wrong.

## Definition

**Input.** An undirected simple graph $G = (V, E)$ on $n$ vertices and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates, with queries.

**Core numbers.** The $k$-core of $G$ is the largest induced subgraph with minimum degree at least $k$; it is unique, and the cores are nested. The core number $\mathrm{core}(v)$ is the largest $k$ with $v$ in the $k$-core. The [k-core decomposition](/k-core-decomposition/) computes all core numbers in $O(n + m)$ time by peeling a vertex of minimum degree again and again.

**Queries.** $\mathrm{core}(v)$ returns the core number of $v$. An $\alpha$-approximate structure returns a value $\tilde c(v)$ with $\mathrm{core}(v) \le \tilde c(v) \le \alpha \cdot \mathrm{core}(v)$, or within a factor $\alpha$ in the other direction.

**Cost.** Update time, worst case or [amortized](/amortized-update-time/). Updates are insertions only, deletions only, or both.

## Variants

- **Insertions only.** Core numbers only grow. See [incremental graphs](/incremental-graph/).
- **Deletions only.** Core numbers only shrink. See [decremental graphs](/decremental-graph/).
- **Fully dynamic.** Both.
- **Batch-dynamic.** A batch of updates arrives at once, often with a parallel algorithm, as in Liu, Shi, Yu, Dhulipala and Shun (2022).
- **Approximate.** Keep each core number within a factor $\alpha$.
- **Hypergraphs and weighted graphs.** Degree is replaced by the number or weight of hyperedges at a vertex.
- **Maximum core only.** Keep the [degeneracy](/degeneracy/), the largest core number.

## Examples

Start with the triangle $0, 1, 2$ and the path $2, 3, 4, 5, 6, 7$. The table gives the core numbers $\mathrm{core}(0), \ldots, \mathrm{core}(7)$ after each update.

| update | core numbers | changed |
|---|---|---|
| start | 2, 2, 2, 1, 1, 1, 1, 1 | |
| insert 73 | 2, 2, 2, 2, 2, 2, 2, 2 | 3, 4, 5, 6, 7 |
| insert 13 | 2, 2, 2, 2, 2, 2, 2, 2 | none |
| insert 03 | 3, 3, 3, 3, 2, 2, 2, 2 | 0, 1, 2, 3 |
| delete 45 | 3, 3, 3, 3, 1, 1, 1, 1 | 4, 5, 6, 7 |
| insert 24 | 3, 3, 3, 3, 2, 1, 1, 1 | 4 |
| delete 01 | 2, 2, 2, 2, 2, 1, 1, 1 | 0, 1, 2, 3 |

The insertion of $73$ closes the cycle $3, 4, 5, 6, 7$, which lifts all five vertices into the 2-core at once. The insertion of $13$ changes nothing: the four vertices $0, 1, 2, 3$ have degrees $2, 3, 3, 2$ among themselves, which is not enough for a 3-core. The next insertion completes $K_4$ on $\{0, 1, 2, 3\}$. Every change is by exactly 1, and in each row only vertices whose core number equalled the smaller core number of the two ends of the edge changed. On a cycle of length $n$, deleting and reinserting one edge changes all $n$ core numbers each time, so an exact structure that lists the changes needs $\Omega(n)$ time per update, even amortized.

## Known algorithms

**Locality.** Sarıyüce et al. (2013) and Li, Yu and Mao (2014) prove the following for an insertion or a deletion of $\{u, v\}$, with $K = \min(\mathrm{core}(u), \mathrm{core}(v))$:

- each core number changes by at most 1;
- only vertices with core number $K$ can change;
- the vertices that change form a connected set that contains an end of the edge with core number $K$, and they are connected to it through vertices of core number $K$.

**Traversal algorithm for an insertion.** Let $r$ be an end with core number $K$. Search from $r$ over vertices of core number $K$, and for each visited vertex $w$ count its neighbors whose core number is at least $K$ and that are not yet ruled out. A vertex whose count is at most $K$ cannot reach $K + 1$, so rule it out and lower the counts of its visited neighbors, which can rule them out too. The visited vertices that are never ruled out get core number $K + 1$. A deletion is symmetric: vertices with core number $K$ near the edge whose count of neighbors with core number at least $K$ drops below $K$ go down to $K - 1$, and the drop can spread. The cost is linear in the size of the searched region, which is small in practice but can be $\Theta(m)$.

**Order-based algorithms.** Zhang, Yu, Zhang and Qin (2017) keep a peeling order of the vertices and repair it after each update. This limits the search to the vertices that come after the root in the order, and is faster in experiments.

**Approximate algorithms with provable bounds.**

| setting | algorithm | factor | update time | case |
|---|---|---|---|---|
| any | recompute by peeling | 1 | $O(n + m)$ | worst, deterministic |
| fully dynamic | traversal or order-based | 1 | $O(m)$ | worst, deterministic |
| insertions only, fully dynamic | Sun, Chan and Sozio (2020) | constant | polylogarithmic | amortized |
| fully dynamic, batches | Liu, Shi, Yu, Dhulipala and Shun (2022) | $2 + \varepsilon$ | polylogarithmic work per update | amortized |

The approximate algorithms place vertices on $O(\log_{1 + \varepsilon} n)$ levels so that a vertex on a level has many neighbors on its level or above, and few neighbors above it. Only vertices that break one of the two conditions move, by one level at a time, and a potential argument bounds the moves. This is the same structure that keeps a low out-degree orientation, and so an approximate [densest subgraph](/dynamic-densest-subgraph/).

## Bounds

**Upper bounds.** Exact: $O(m)$ per update in the worst case. Approximate: a factor $2 + \varepsilon$ with polylogarithmic amortized time per update.

**Lower bounds.** The cycle example shows that exact maintenance has $\Omega(n)$ changes per update in the worst case, even amortized, so exact core numbers cannot all be kept explicitly in sublinear time per update. Approximate core numbers avoid this, because a factor $2$ allows a vertex to keep its value while the exact value moves between $1$ and $2$.

## Reductions

- **To densest subgraph.** The maximum core number lies between $\rho^*$ and $2\rho^*$, where $\rho^*$ is the maximum density, so approximate cores give an approximate [densest subgraph](/dynamic-densest-subgraph/).
- **To orientations and coloring.** A vertex of core number $k$ has at most $k$ neighbors later in the peeling order, so orienting edges along the order gives out-degree at most the degeneracy, and greedy coloring in the reverse order uses at most degeneracy plus 1 colors; see [dynamic graph coloring](/dynamic-graph-coloring/).

## Applications

- **Network analysis.** Core numbers rank vertices by how deep they sit in dense parts of a social, web or biological network, and these networks change all the time.
- **Influence and spreading.** Vertices of high core number are good seeds for spreading processes.
- **Community search.** Find a connected $k$-core that contains a given vertex, in a changing graph.
- **Subroutine.** Degeneracy orders speed up clique listing and other dense-subgraph searches.

## References
