---
tag: 637H34
kind: problem
slug: decremental-connectivity
name: Decremental connectivity
aliases:
- deletions-only connectivity
area: graphs/dynamic-graphs
level: advanced
summary: Maintain connected components under edge deletions only.
prereqs: [decremental-graph, connected-components, breadth-first-search]
see_also: [dynamic-connectivity, incremental-connectivity, even-shiloach-tree, offline-dynamic-connectivity, decremental-sssp, holm-de-lichtenberg-thorup]
sources:
  - paper: doi:10.1145/322234.322235
    title: Shimon Even and Yossi Shiloach, An on-line edge-deletion problem, Journal of the ACM 28(1), 1 to 4 (1981)
    locator: the whole paper (the two processes run in parallel, O(q + nm) total time for general graphs and the smaller-side bound for forests)
  - paper: doi:10.1006/jagm.1999.1033
    title: Mikkel Thorup, Decremental dynamic connectivity, Journal of Algorithms 33(2), 229 to 243 (1999)
    locator: the main theorem (randomized, O(m log(n^2/m) + n polylog n) expected total time)
  - paper: doi:10.1016/S0020-0190(97)00170-1
    title: Stephen Alstrup, Jens Peter Secher and Maz Spork, Optimal on-line decremental connectivity in trees, Information Processing Letters 64(4), 161 to 164 (1997)
    locator: the whole paper (O(n) total time and O(1) query time on a tree)
  - paper: doi:10.1007/s00224-016-9709-x
    title: Jakub Łącki and Piotr Sankowski, Optimal decremental connectivity in planar graphs, Theory of Computing Systems 61(4), 1037 to 1053 (2017)
    locator: the main theorem (O(n) total update time and O(1) query time for planar graphs)
---

Decremental connectivity is the problem of answering "are $u$ and $v$ connected?" in an undirected [decremental graph](/decremental-graph/), where edges are deleted one at a time and never inserted. Components can only split, so each vertex changes its component a bounded number of times, and the cost is usually measured as the total time over all deletions. Even and Shiloach (1981) gave the first algorithm, with $O(1)$ query time and $O(mn)$ total update time on general graphs. It is a special case of [dynamic connectivity](/dynamic-connectivity/), and on special classes such as trees and planar graphs it can be solved in linear total time.

## In plain words

A network loses links one at a time and never gets new ones. After each loss, people ask whether two places can still reach each other.

Most of the time a lost link changes nothing, because another route exists. Sometimes a group falls apart into two groups. Then every place in one of the two parts needs a new group name. The trick is to rename only the smaller part. To find it, search both sides at the same pace, and stop as soon as one side runs out of places. A place is renamed only when its group at least halves, so it is renamed only a few times over the whole run. The hard part is to notice quickly when a lost link changes nothing.

## Definition

**Input.** An undirected graph $G_0 = (V, E_0)$ with $n = |V|$ and $m = |E_0|$, then an online sequence of operations:

- $\mathrm{delete}(e)$ for an edge $e$ of the current graph, which removes it,
- $\mathrm{connected}(u, v)$, which returns true if and only if $u$ and $v$ are in the same component of the current graph.

**Output.** The answer to each query before the next operation is read.

**Cost.** The preprocessing time, the **total update time** over a sequence of up to $m$ deletions, and the query time. A total update time $T(n, m)$ is $T(n, m)/m$ [amortized](/amortized-update-time/) per deletion.

A common form of the structure keeps a label $c(v)$ for each vertex, equal for two vertices exactly when they are connected. Then a query compares two labels in $O(1)$ time, and the update must fix the labels after each split.

## Variants

- **Trees and forests.** The graph is a forest, so each deletion splits a tree.
- **Planar graphs.** The graph is planar, often with a fixed embedding.
- **Vertex deletions.** A deletion removes a vertex with all its edges.
- **Offline.** All deletions are known in advance. Reverse the sequence and insert the edges with a [disjoint-set](/disjoint-set/) structure, from the final graph back to $G_0$; this takes $O(m\,\alpha(n))$ time plus the time to read the input.
- **Decremental strong connectivity and reachability.** The directed versions; see [dynamic reachability](/dynamic-reachability/).
- **Decremental distances.** Keep distances instead of connectivity; see [decremental single-source shortest paths](/decremental-sssp/).

## Examples

**A run.** Take the 8-cycle $0, 1, \ldots, 7$ with the chords $04$ and $26$, so $m = 10$, and delete the edges in the order shown.

| deleted edge | effect | parts after a split | components |
|---|---|---|---|
| 04 | no split | | 1 |
| 01 | no split | | 1 |
| 45 | no split | | 1 |
| 26 | split | $\{1, 2, 3, 4\}$ and $\{0, 5, 6, 7\}$ | 2 |
| 23 | split | $\{1, 2\}$ and $\{3, 4\}$ | 3 |
| 67 | split | $\{5, 6\}$ and $\{0, 7\}$ | 4 |

The first three deletions change nothing, because a cycle still holds each deleted edge's ends together. The labelling structure must still spend time to find this out. At the fourth deletion both sides have 4 vertices, so either can be relabeled. At the last two deletions, a relabeling of the smaller side changes 2 labels each.

**A forest.** In a forest each deletion splits a tree. On a path of $n$ vertices, deleting the middle edge, then the middle edges of the two halves, and so on, relabels about $n/2$ vertices per round for $\log_2 n$ rounds, so about $(n/2)\log_2 n$ labels in total. This is the worst case of the smaller-side rule.

## Known algorithms

**Even and Shiloach (1981).** After deleting $\{u, v\}$, run two processes in parallel, one step of each in turn, and stop both when one of them finishes.

- **Process A** runs two searches, from $u$ and from $v$, in lockstep, one edge of each in turn. If one search reaches the start of the other, the component did not split. If one search finishes its whole side first, that side is the smaller one, and A gives its vertices a new label.
- **Process B** keeps a [breadth-first search](/breadth-first-search/) tree with levels from a fixed root of each component, and repairs the levels after the deletion. If a vertex loses its last neighbor at the level above, its level goes up, and the change can push the levels of its children up too. If the component did not split, B ends with a correct tree. This is the [Even-Shiloach tree](/even-shiloach-tree/).

Process A costs, per deletion that splits, at most twice the number of vertices and edges of the smaller side, plus a constant. A vertex or edge is on the smaller side only when the size of its component (in vertices plus edges) drops to at most half, which can happen at most $\log_2(n + m)$ times. So the total cost of A over all splits is $O((n + m)\log n)$. Process B costs $O(mn)$ in total, because each vertex level only grows, is at most $n$, and each level change of a vertex costs time proportional to its degree. A deletion that does not split ends when B finishes, and its cost is at most twice the work of B. A deletion that splits ends when A finishes, and its cost is at most twice the work of A; the tree of B is then rebuilt on the smaller part and kept on the larger part, where its levels still only grow. Even and Shiloach show that the total is $O(q + mn)$ for $q$ queries, for a deterministic algorithm and for every sequence. On a forest, process A alone gives $O(n \log n)$ total.

**Faster algorithms.**

| graph class | total update time | query | case | source |
|---|---|---|---|---|
| general | $O(mn)$ | $O(1)$ | worst, deterministic | Even and Shiloach (1981) |
| general | $O(m \log(n^2/m) + n \operatorname{polylog} n)$ | $O(1)$ | expected, randomized | Thorup (1999) |
| general | via fully dynamic structures, $O(m \log^2 n)$ | $O(\log n / \log\log n)$ | amortized, deterministic | [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/) (2001) |
| trees | $O(n)$ | $O(1)$ | word RAM, deterministic | Alstrup, Secher and Spork (1997) |
| planar | $O(n)$ | $O(1)$ | deterministic | Łącki and Sankowski (2017) |

Thorup's bound is $O(m)$ total, so $O(1)$ amortized per deletion, when $m = \Theta(n^2)$. For dense graphs this is optimal, since the input already has size $m$.

## Bounds

**Upper bounds.** As in the table. On general sparse graphs the best total bounds are polylogarithmic per deletion; for dense graphs, Thorup's algorithm gives constant amortized time per deletion.

**Lower bounds.** Each algorithm must read the input, so $\Omega(m)$ total time is necessary, and the tree and planar algorithms are optimal. The $\Omega(\log n)$ cell-probe bound of Pătraşcu and Demaine for [dynamic connectivity](/dynamic-connectivity-lower-bound/) is proved with both insertions and deletions, so it does not directly apply to the deletions-only problem, and the trees result shows that a deletions-only problem on forests is easier than the fully dynamic one.

## Reductions

- **To fully dynamic connectivity.** Every fully dynamic structure solves the decremental problem with the same bounds.
- **Offline decremental to incremental.** With all deletions known in advance, reverse the order and use [incremental connectivity](/incremental-connectivity/).
- **From decremental connectivity to decremental distances.** Connectivity is the question "is the distance finite?", so a [decremental SSSP](/decremental-sssp/) structure from each component root answers it. The Even-Shiloach algorithm is built on exactly this view.

## Applications

- **Network reliability.** Follow how a network falls apart as links fail, with no repairs.
- **Graph algorithms that remove edges.** Some decomposition and pruning methods delete edges and ask, after each deletion, whether the graph is still connected or which part a vertex is in.
- **Building block.** The smaller-side search of process A is a standard tool in decremental algorithms for strongly connected components and for expanders.

## References
