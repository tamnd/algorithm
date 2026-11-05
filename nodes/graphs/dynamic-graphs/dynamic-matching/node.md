---
tag: 3TZFXE
kind: problem
slug: dynamic-matching
name: Dynamic matching
aliases:
- fully dynamic matching
area: graphs/dynamic-graphs
level: research
summary: Maintain a maximum or approximate maximum matching under edge updates.
prereqs: [dynamic-graph, maximum-matching, maximal-matching, augmenting-path]
see_also: [gupta-peng-dynamic-matching, dynamic-vertex-cover, hopcroft-karp, edmonds-blossom, omv-conjecture, amortized-update-time, dynamic-densest-subgraph]
sources:
  - paper: doi:10.1145/1806689.1806753
    title: Krzysztof Onak and Ronitt Rubinfeld, Maintaining a large matching and a small vertex cover, Proceedings of STOC 2010, 457 to 464
    locator: the main theorem (constant-factor approximation in O(log^2 n) expected amortized time per update)
  - paper: doi:10.1137/130914140
    title: Surender Baswana, Manoj Gupta and Sandeep Sen, Fully dynamic maximal matching in O(log n) update time, SIAM Journal on Computing 44(1), 88 to 113 (2015); corrected version in SIAM Journal on Computing 47(3), 617 to 650 (2018), doi:10.1137/16m1106158
    locator: the main theorem (maximal matching in O(log n) expected amortized time, against an oblivious adversary)
  - paper: doi:10.1109/focs.2016.43
    title: Shay Solomon, Fully dynamic maximal matching in constant update time, Proceedings of FOCS 2016, 325 to 334
    locator: the main theorem (maximal matching in O(1) expected amortized time, against an oblivious adversary)
  - paper: doi:10.1145/2700206
    title: Ofer Neiman and Shay Solomon, Simple deterministic algorithms for fully dynamic maximal matching, ACM Transactions on Algorithms 12(1), 1 to 15 (2015)
    locator: the main theorem (deterministic maximal matching in O(m^(1/2)) worst-case time per update)
  - paper: doi:10.1145/2746539.2746609
    title: Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, Proceedings of STOC 2015, 21 to 30
    locator: the table of results (conditional lower bounds for maximum matching)
---

The dynamic matching problem asks to keep a [matching](/maximum-matching/) of an undirected [dynamic graph](/dynamic-graph/), a set of edges with no common end, as large as possible while edges are inserted and deleted. Exact maximum matchings are hard to keep: one update can call for a long [augmenting path](/augmenting-path/), and the problem has polynomial conditional lower bounds. A [maximal matching](/maximal-matching/), which is at least half of the maximum, can be kept in $O(1)$ expected amortized time with a randomized algorithm, and a $(1 + \varepsilon)$-approximation in $O(m^{1/2})$ worst-case time with a deterministic one. Much current work is on approximation factors between 1 and 2 with small update time.

## In plain words

Pair up people for a task, where each person can only be paired with someone they know. You want as many pairs as possible. People meet and fall out over time.

When two unpaired people meet, pair them. When a pair falls out, each of the two may find a new unpaired partner. This simple rule never leaves two unpaired people who know each other, and it gets at least half the best number of pairs. Getting the best number exactly is harder: a single new acquaintance can mean that a whole chain of people must swap partners.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices, at first with no edges, and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates.

**Output.** After each update, a matching $M \subseteq E$, with queries $\mathrm{mate}(v)$ and $|M|$. Let $\nu(G)$ be the size of a maximum matching. An $\alpha$-approximate structure keeps $|M| \ge \nu(G)/\alpha$. Some structures only keep an estimate of $\nu(G)$, not a matching.

**Cost.** Update time, worst case or [amortized](/amortized-update-time/), and the type of adversary: an **oblivious** adversary fixes the update sequence in advance, and an **adaptive** one may choose updates after it sees the current matching. Deterministic algorithms work against both. Updates are insertions only, deletions only, or both.

## Variants

- **Maximum matching.** $\alpha = 1$.
- **Maximal matching.** No edge has both ends free; this gives $\alpha = 2$.
- **Approximate.** $\alpha = 1 + \varepsilon$, $3/2$, $2 + \varepsilon$, and others.
- **Size only.** Keep an estimate of $\nu(G)$.
- **Bipartite graphs.** Some algebraic and flow-based results hold only here.
- **Weighted.** Keep a matching of near-maximum total weight; see [maximum weight matching](/maximum-weight-matching/).
- **Vertex updates.** In the bipartite online setting, vertices of one side arrive with their edges.

## Examples

Take $V = \{0, \ldots, 5\}$ and the rule: on an insertion with both ends free, match them; on the deletion of a matched edge, let each freed end take its smallest free neighbor, if any.

| update | matching kept | size | $\nu(G)$ |
|---|---|---|---|
| insert 01 | 01 | 1 | 1 |
| insert 12 | 01 | 1 | 1 |
| insert 23 | 01, 23 | 2 | 2 |
| insert 34 | 01, 23 | 2 | 2 |
| insert 45 | 01, 23, 45 | 3 | 3 |
| delete 01 | 23, 45 | 2 | 2 |
| insert 05 | 23, 45 | 2 | 3 |
| delete 34 | 23, 45 | 2 | 2 |

After the insertion of $05$ the graph is the path $1, 2, 3, 4, 5, 0$, and the kept matching is maximal but not maximum. The path itself is an augmenting path: it starts and ends at free vertices and alternates between unmatched and matched edges. Flipping it gives the maximum matching $12, 34, 50$, but it changes all five edges of the path. So an exact structure can be forced to change $\Theta(n)$ edges for one update.

## Known algorithms

| factor | algorithm | update time | case | deterministic |
|---|---|---|---|---|
| 1 | recompute with [Hopcroft-Karp](/hopcroft-karp/) or [Edmonds](/edmonds-blossom/) | $O(m n^{1/2})$ or more | worst | yes |
| 1 | search for one augmenting path per update | $O(m)$ | worst | yes |
| constant | Onak and Rubinfeld (2010) | $O(\log^2 n)$ | expected amortized | no |
| 2, maximal | Baswana, Gupta and Sen (2011, 2015) | $O(\log n)$ | expected amortized | no |
| 2, maximal | Solomon (2016) | $O(1)$ | expected amortized | no |
| 2, maximal | Neiman and Solomon (2013, 2015) | $O(m^{1/2})$ | worst | yes |
| $1 + \varepsilon$ | [Gupta and Peng](/gupta-peng-dynamic-matching/) (2013) | $O(m^{1/2} \varepsilon^{-2})$ | worst | yes |

**One augmenting path per update.** The size $\nu(G)$ changes by at most 1 per update. After an insertion, a maximum matching stays maximum or needs one augmenting path, and after a deletion of a matched edge, at most one augmenting path restores it. So one search for an augmenting path, $O(m)$ time with a blossom-aware search, keeps a maximum matching.

**Maximal matching with levels.** Baswana, Gupta and Sen put each vertex on a level. A vertex on a high level is matched to a partner chosen at random among many neighbors, so the adversary, which cannot see the choice, needs many deletions to hit the matched edge. When it does, the work to rematch is paid for by the many updates before. Solomon (2016) refines this to $O(1)$ expected amortized time.

**Approximate matching with a small certificate.** Gupta and Peng compute a $(1 + \varepsilon)$-approximate matching from scratch and then keep it, with small repairs, for $\varepsilon |M|$ updates; this is enough while the matching is large, and a degree bound handles small matchings.

## Bounds

**Upper bounds.** As in the table. For a maximal matching, $O(1)$ expected amortized time is optimal up to the constant.

**Conditional lower bounds.** Henzinger, Krinninger, Nanongkai and Saranurak (2015) show, under the [OMv conjecture](/omv-conjecture/), polynomial lower bounds for keeping the exact size of a maximum matching, even in bipartite graphs. So small update time for $\alpha = 1$ is not expected.

**Recourse.** The example shows that an exact matching can need $\Theta(n)$ edge changes per update. Approximate matchings can be kept with $O(1)$ amortized changes.

## Reductions

- **Vertex cover.** The ends of a maximal matching form a [vertex cover](/vertex-cover/) of size at most twice the minimum, so a dynamic maximal matching gives a 2-approximate [dynamic vertex cover](/dynamic-vertex-cover/).
- **Fractional matching.** Many algorithms first keep a fractional matching, a weight on each edge with total weight at most 1 at each vertex, and round it. The fractional problem is the linear programming dual of fractional vertex cover.
- **Orientations.** In graphs with small [arboricity](/arboricity/), a low out-degree orientation lets each vertex check only its out-neighbors for free partners, which gives fast maximal matching; see [dynamic densest subgraph](/dynamic-densest-subgraph/).

## Applications

- **Ride sharing and online markets.** Drivers and riders, or buyers and sellers, come and go, and the platform keeps a large set of pairs.
- **Network switches.** Inputs and outputs of a switch are matched at each step while traffic changes.
- **Subroutine.** Dynamic matchings and vertex covers are parts of dynamic algorithms for set cover, scheduling and clustering.

## References
