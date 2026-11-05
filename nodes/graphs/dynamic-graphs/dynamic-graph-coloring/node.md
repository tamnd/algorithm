---
tag: MSB69K
kind: problem
slug: dynamic-graph-coloring
name: Dynamic graph coloring
aliases:
- dynamic vertex coloring
area: graphs/dynamic-graphs
level: research
summary: Maintain a proper vertex coloring with few colors under edge updates.
prereqs: [dynamic-graph, graph-coloring, greedy-coloring, amortized-update-time]
see_also: [chromatic-number, online-graph-coloring-problem, edge-coloring, arboricity, dynamic-densest-subgraph, dynamic-bipartiteness, maximal-independent-set]
sources:
  - paper: doi:10.1137/1.9781611975031.1
    title: Sayan Bhattacharya, Deeparnab Chakrabarty, Monika Henzinger and Danupon Nanongkai, Dynamic algorithms for graph coloring, Proceedings of SODA 2018, 1 to 20
    locator: the three main results ((Delta + 1)-vertex coloring in O(log Delta) expected amortized time; (1 + o(1)) Delta colors deterministically; (2 Delta - 1)-edge coloring in O(log Delta) worst-case time)
  - paper: doi:10.1145/3501403
    title: Monika Henzinger and Pan Peng, Constant-time dynamic (Delta + 1)-coloring, ACM Transactions on Algorithms 18(2), 1 to 21 (2022)
    locator: the main theorem (O(1) expected amortized time, Las Vegas) and the Omega(log n) lower bound for deciding Delta-colorability
  - paper: doi:10.1145/3494539
    title: Sayan Bhattacharya, Fabrizio Grandoni, Janardhan Kulkarni, Quanquan C. Liu and Shay Solomon, Fully dynamic (Delta + 1)-coloring in O(1) update time, ACM Transactions on Algorithms 18(2), 1 to 25 (2022)
    locator: the main theorem (O(1) expected amortized update time)
  - paper: doi:10.1007/s00453-018-0473-y
    title: Luis Barba, Jean Cardinal, Matias Korman, Stefan Langerman, André van Renssen, Marcel Roeloffzen and Sander Verdonschot, Dynamic graph coloring, Algorithmica 81(4), 1319 to 1341 (2019)
    locator: the two trade-off algorithms and the lower bound on recolorings for dynamic forests
  - paper: doi:10.1145/3392724
    title: Shay Solomon and Nicole Wein, Improved dynamic graph coloring, ACM Transactions on Algorithms 16(3), 1 to 24 (2020)
    locator: the trade-off with polylog n colors and O(1) recolorings, and the O(alpha log^2 n)-coloring for arboricity alpha in O(1) amortized time
---

Dynamic graph coloring is the problem of keeping a proper vertex [coloring](/graph-coloring/) of an undirected [dynamic graph](/dynamic-graph/), so that the two ends of each edge have different colors, while edges are inserted and deleted. Finding or even approximating the [chromatic number](/chromatic-number/) is NP-hard, so dynamic algorithms either aim for a number of colors in terms of a simple parameter, such as $\Delta + 1$ for maximum degree $\Delta$, or study how many vertices must change color per update. A $(\Delta + 1)$-coloring can be kept in $O(1)$ expected amortized time per update with a randomized algorithm.

## In plain words

Give each person in a network a color so that no two friends share a color. As friendships start and end, keep the rule true and do not use too many colors.

If two friends with the same color become friends, one of them needs a new color. Someone with few friends can always find a free color among a small palette. The trouble is that a careless choice can force many later changes. Changing colors also has a cost of its own, because each change may mean moving a job, a frequency or a slot. So there is a trade-off between the number of colors and the number of changes per update.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices and an online sequence of edge updates $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$; some versions also insert and delete vertices.

**Output.** After each update, a map $c : V \to \{1, \ldots, k\}$ with $c(u) \ne c(v)$ for each edge $\{u, v\} \in E$, and a query $\mathrm{color}(v)$ that returns $c(v)$.

**Measures.** The number of colors $k$, given as a function of $\Delta$, of the [arboricity](/arboricity/) or of the chromatic number; the update time, worst case or [amortized](/amortized-update-time/); and the **recourse**, the number of vertices whose color changes per update.

Deletions never break a proper coloring, so the work is in insertions and in keeping $k$ small as the graph changes. When $\Delta$ is not fixed in advance, an algorithm may need to use more colors when $\Delta$ grows, and to free them when it shrinks.

## Variants

- **Insertions only.** Close to [online coloring](/online-graph-coloring-problem/), but here recoloring is allowed.
- **Fully dynamic.** Insertions and deletions, the main setting.
- **$(\Delta + 1)$ colors.** The number of colors that [greedy coloring](/greedy-coloring/) always achieves.
- **Colors in terms of the chromatic number.** With black-box access to a static algorithm that colors any subgraph with $C$ colors, keep a coloring with a function of $C$ colors and few recolorings.
- **Sparse graphs.** Colors in terms of the arboricity $\alpha$, or the [degeneracy](/degeneracy/).
- **Edge coloring.** Keep a proper [edge coloring](/edge-coloring/); $2\Delta - 1$ colors is the greedy bound and $\Delta + 1$ the bound of [Vizing's theorem](/vizing-theorem/).

## Examples

Start with the paths $0, 1, 2$ and $3, 4, 5$, colored $c = (0, 1, 0, 0, 1, 0)$. On a conflict, the rule recolors the second end with the smallest color in $\{0, \ldots, \Delta\}$ that none of its neighbors has.

| update | $\Delta$ | colors $c(0), \ldots, c(5)$ | recolored |
|---|---|---|---|
| insert 23 | 2 | 0, 1, 0, 2, 1, 0 | 3 |
| insert 50 | 2 | 2, 1, 0, 2, 1, 0 | 0 |
| insert 14 | 3 | 2, 1, 0, 2, 3, 0 | 4 |
| delete 23 | 3 | 2, 1, 0, 2, 3, 0 | none |
| insert 03 | 3 | 2, 1, 0, 0, 3, 0 | 3 |
| insert 24 | 4 | 2, 1, 0, 0, 3, 0 | none |

After the second update the graph is the 6-cycle $0, 1, 2, 3, 4, 5$, which is bipartite, but the coloring uses 3 colors. To keep 2 colors at the first update, the whole path $3, 4, 5$ would have to swap colors: 3 recolorings in place of 1. On a long path, one insertion can force about $n/2$ recolorings for a 2-coloring. This is the phenomenon behind the lower bound of Barba et al. below.

## Known algorithms

**Greedy repair.** On an insertion of $\{u, v\}$ with $c(u) = c(v)$, recolor $v$ with a color in $\{1, \ldots, \Delta + 1\}$ not used by its neighbors. Each vertex has at most $\Delta$ neighbors, so such a color exists. A scan of the neighbors costs $O(\deg v)$, so this is $O(\Delta)$ worst-case time per update and recourse 1, deterministic. The fast algorithms avoid the scan.

| colors | algorithm | update time | case | deterministic |
|---|---|---|---|---|
| $\Delta + 1$ | greedy repair | $O(\Delta)$ | worst | yes |
| $\Delta + 1$ | Bhattacharya, Chakrabarty, Henzinger and Nanongkai (2018) | $O(\log \Delta)$ | expected amortized | no |
| $(1 + o(1))\Delta$ | Bhattacharya, Chakrabarty, Henzinger and Nanongkai (2018) | $O(\mathrm{poly}\log \Delta)$ | amortized | yes |
| $\Delta + 1$ | Henzinger and Peng (2022); Bhattacharya, Grandoni, Kulkarni, Liu and Solomon (2022) | $O(1)$ | expected amortized | no |
| $O(\alpha \log^2 n)$ | Solomon and Wein (2020) | $O(1)$ | amortized | yes |

**Randomized colors.** A useful idea is to recolor a vertex with a random color among those free in its neighborhood. An adversary that does not see the random choices then needs many updates before it hits a vertex's color by chance. Henzinger and Peng give each vertex a random rank and let low-rank vertices yield, which avoids the hierarchical decomposition of the 2018 algorithm.

**Sparse graphs.** A low out-degree orientation lets each vertex check only its out-neighbors. Solomon and Wein build on a refined orientation structure of this kind to keep $O(\alpha \log^2 n)$ colors in $O(1)$ amortized time, deterministic.

## Bounds

**Recourse trade-off.** Barba et al. show that any algorithm that keeps a $C$-coloring of an $n$-vertex dynamic forest, for a constant $C \ge 2$, must recolor $\Omega(n^{2/(C(C-1))})$ vertices per update in the amortized sense. For $C = 2$ this is $\Omega(n)$, as the path example suggests. Their two algorithms trade colors against recolorings in the other direction, and Solomon and Wein get a $\tilde O(C \beta \log^2 n)$-coloring with $O(\beta)$ recolorings per update, for any $\beta > 0$, where $C$ is the number of colors of the static black box.

**Time lower bound.** Henzinger and Peng show that deciding whether a graph with maximum degree at most $\Delta$ has a $\Delta$-coloring takes $\Omega(\log n)$ time per operation, so $\Delta + 1$ colors in constant time is the right target.

**Hardness of the number of colors.** For general graphs, approximating the chromatic number within $n^{1 - \varepsilon}$ is NP-hard already in the static case, so no efficient dynamic algorithm keeps a coloring with close to $\chi(G)$ colors unless P = NP.

## Reductions

- **From bipartiteness.** Keeping a 2-coloring is possible exactly while the graph is bipartite; see [dynamic bipartiteness](/dynamic-bipartiteness/). The recourse bound above shows that keeping the 2-coloring itself, not only the answer, can be expensive.
- **To orientations.** Bounds in terms of arboricity use a dynamic low out-degree orientation, the dual of the [densest subgraph](/dynamic-densest-subgraph/) problem.
- **Maximal independent sets.** In a coloring where each vertex has the smallest color not used by its neighbors, the first color class is a [maximal independent set](/maximal-independent-set/), and each later class is one in the graph left after the earlier classes are removed. So such a coloring is at least as hard to keep as a maximal independent set.

## Applications

- **Frequency and channel assignment.** Radio stations or Wi-Fi access points that interfere get different channels, and the set of links changes as devices move.
- **Scheduling with conflicts.** Jobs that use a common resource get different time slots, and conflicts appear and go away.
- **Register allocation.** In compilers, variables that are live at the same time get different registers; incremental compilers change the interference graph.

## References
