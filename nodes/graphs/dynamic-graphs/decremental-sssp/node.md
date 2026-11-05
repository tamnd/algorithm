---
tag: CS86G1
kind: problem
slug: decremental-sssp
name: Decremental single-source shortest paths
aliases:
- decremental SSSP
area: graphs/dynamic-graphs
level: research
summary: Maintain shortest-path distances from a source under edge deletions only.
prereqs: [decremental-graph, dynamic-single-source-shortest-paths, breadth-first-search]
see_also: [even-shiloach-tree, decremental-connectivity, dynamic-reachability, dynamic-all-pairs-shortest-paths, oblivious-adversary, adaptive-adversary, omv-conjecture]
sources:
  - paper: doi:10.1145/322234.322235
    title: Shimon Even and Yossi Shiloach, An on-line edge-deletion problem, Journal of the ACM 28(1), 1 to 4 (1981)
    locator: the breadth-first tree with levels that only grow (O(mn) total time)
  - paper: doi:10.1109/SFFCS.1999.814580
    title: Valerie King, Fully dynamic algorithms for maintaining all-pairs shortest paths and transitive closure in digraphs, Proceedings of FOCS 1999, 81 to 89
    locator: the decremental shortest-path tree for directed graphs with integer weights (O(mD) total time for depth D)
  - paper: doi:10.1145/3218657
    title: Monika Henzinger, Sebastian Krinninger and Danupon Nanongkai, Decremental single-source shortest paths on undirected graphs in near-linear total update time, Journal of the ACM 65(6), 1 to 40 (2018)
    locator: the main theorem ((1 + epsilon)-approximate, m^(1+o(1)) expected total time, oblivious adversary)
  - paper: doi:10.1145/2897518.2897521
    title: Aaron Bernstein and Shiri Chechik, Deterministic decremental single source shortest paths, beyond the O(mn) bound, Proceedings of STOC 2016, 389 to 397
    locator: the main theorem (deterministic (1 + epsilon)-approximate, unweighted undirected graphs)
  - paper: doi:10.1109/FOCS52979.2021.00100
    title: Aaron Bernstein, Maximilian Probst Gutenberg and Thatchaphol Saranurak, Deterministic decremental SSSP and approximate min-cost flow in almost-linear time, Proceedings of FOCS 2021, 1000 to 1008
    locator: the main theorem (deterministic (1 + epsilon)-approximate, weighted undirected graphs, m^(1+o(1)) total time)
  - paper: doi:10.1145/2746539.2746609
    title: Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, Proceedings of STOC 2015, 21 to 30
    locator: the table of results (conditional lower bounds for partially dynamic shortest paths)
---

Decremental single-source shortest paths is the problem of keeping the distances $d(s, v)$ from a fixed source $s$ in a [decremental graph](/decremental-graph/), where edges are only deleted or made heavier. Distances can only grow, so the cost is measured as the total time over all deletions. The classic exact algorithm, the Even-Shiloach tree, takes $O(mn)$ total time on unweighted graphs, and conditional lower bounds suggest this is close to optimal for exact distances. Research since 2014 has found $(1 + \varepsilon)$-approximate algorithms with almost-linear total time, first randomized against an oblivious adversary and later deterministic.

## In plain words

Roads in a country close one after another, and none reopen. A map shows, for each town, how far it is from the capital. After each closure, the map must be correct again.

Since roads only close, every distance can only grow or stay. So each town's distance climbs step by step, and it cannot climb more than a fixed number of times before the town is cut off. A simple method pays for each step of each town. That is fast when distances are short, but slow on large maps. Newer methods allow a small error, such as one percent, and then need only a little more time than reading the map once.

## Definition

**Input.** A graph $G_0 = (V, E_0)$, directed or undirected, with $n$ vertices, $m$ edges and nonnegative weights, a source $s$, and an online sequence of operations:

- $\mathrm{delete}(e)$, or $\mathrm{increase}(e, x)$, which raises the weight of $e$ to $x$,
- $\mathrm{dist}(v)$, which returns $d(s, v)$ in the current graph.

**Output.** The answer to each query before the next operation is read. An **$\alpha$-approximate** algorithm returns $\tilde d(v)$ with $d(s, v) \le \tilde d(v) \le \alpha \cdot d(s, v)$.

**Cost.** Preprocessing, total update time over all deletions, and query time. A total time $T$ is $T/m$ [amortized](/amortized-update-time/) per deletion.

**Adversary.** A randomized algorithm may assume an [oblivious adversary](/oblivious-adversary/), which fixes the deletions in advance, or allow an [adaptive adversary](/adaptive-adversary/), which picks each deletion after it sees the answers. Many uses of decremental SSSP inside other algorithms need the adaptive kind, because the deletions depend on the answers.

## Variants

- **Unweighted or weighted.** Distances are numbers of edges, or sums of weights.
- **Undirected or directed.** The directed problem is harder; even reachability, the question $d(s, v) < \infty$, is a separate problem; see [dynamic reachability](/dynamic-reachability/).
- **Exact or approximate.**
- **Bounded depth.** Track only distances up to a bound $D$, and report the others as larger than $D$.
- **Incremental.** Insertions only; Roditty and Zwick show that the conditional lower bounds below hold for it too. See [dynamic single-source shortest paths](/dynamic-single-source-shortest-paths/).

## Examples

Take the unweighted undirected graph on $\{0, \ldots, 6\}$ with edges $01, 02, 12, 13, 23, 24, 35, 45, 46, 56$, and source $0$. The distances start at $(0, 1, 1, 2, 2, 3, 3)$. The last column is the sum of the increases of the finite distances, which is the number of single level steps that an Even-Shiloach tree makes.

| deleted edge | distances after it | total increase |
|---|---|---|
| 24 | 0, 1, 1, 2, 4, 3, 4 | 3 |
| 02 | 0, 1, 2, 2, 4, 3, 4 | 1 |
| 13 | 0, 1, 2, 3, 5, 4, 5 | 4 |
| 46 | 0, 1, 2, 3, 5, 4, 5 | 0 |
| 12 | 0, 1, ∞, ∞, ∞, ∞, ∞ | 0 |

Deleting $24$ moves vertex 4 two levels down and vertex 6 one level, through the longer route $0, 1, 3, 5, 4$. Deleting $46$ changes nothing, because 6 still has a neighbor, 5, one level above it. Deleting $12$ cuts off five vertices at once; they leave the tree, and their levels no longer count.

## Known algorithms

**Even-Shiloach tree.** Keep a level $\ell(v) = d(s, v)$ for each vertex. When $v$ loses its last neighbor at level $\ell(v) - 1$, raise $\ell(v)$ by one and check its neighbors, which may need to rise too. A level only grows and is at most $n$ before the vertex is cut off, and each step of $v$ costs $O(\deg v)$ time, so the total is $O(mn)$, deterministic. King (1999) extends this to directed graphs and to positive integer weights with depth bound $D$, in $O(mD)$ total time.

| graph | approximation | total time | case | deterministic |
|---|---|---|---|---|
| unweighted, directed or undirected | exact | $O(mn)$ | worst | yes |
| integer weights, depth $D$ | exact | $O(mD)$ | worst | yes |
| weighted undirected, Henzinger, Krinninger and Nanongkai (2014) | $1 + \varepsilon$ | $m^{1 + o(1)}$ | expected, oblivious adversary | no |
| unweighted undirected, Bernstein and Chechik (2016) | $1 + \varepsilon$ | $\tilde O(n^2)$ | worst | yes |
| weighted undirected, Bernstein, Probst Gutenberg and Saranurak (2021) | $1 + \varepsilon$ | $m^{1 + o(1)}$ | worst | yes |

**Approximate algorithms.** The fast approximate algorithms combine two ideas. First, an Even-Shiloach tree is cheap when distances are small, so they run it on a graph where long paths are shortened, for example with a hop set or with contracted clusters. Second, the error from these shortcuts is kept to a factor $1 + \varepsilon$ by a careful choice of scales. The deterministic algorithms replace random choices with expander decompositions, which also makes them work against an adaptive adversary.

**Directed graphs.** For directed graphs, Henzinger, Krinninger and Nanongkai (2014) gave the first algorithms with total time polynomially below $mn$, and later work improved the exponent; these bounds are still far from linear.

## Bounds

**Upper bounds.** As in the table: $O(mn)$ exact, and $m^{1 + o(1)}$ for $(1 + \varepsilon)$-approximation in undirected graphs, deterministic.

**Conditional lower bounds.** Roditty and Zwick (2004) reduce Boolean matrix multiplication to exact decremental SSSP in unweighted graphs, so a combinatorial algorithm much faster than $mn$ in total would give a fast combinatorial matrix multiplication. Henzinger, Krinninger, Nanongkai and Saranurak (2015) prove bounds of the same kind under the [OMv conjecture](/omv-conjecture/), which covers all algorithms, not only combinatorial ones. So the gap between exact and approximate distances is believed to be real.

## Reductions

- **Decremental connectivity.** $d(s, v) < \infty$ exactly when $v$ is in the component of $s$, so [decremental connectivity](/decremental-connectivity/) is a special case, and the Even-Shiloach tree first appeared as a part of a connectivity algorithm.
- **All pairs.** One structure per source gives decremental all-pairs distances in $n$ times the time; see [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/).
- **Weights to unweighted.** Replace an edge of integer weight $w$ by a path of $w$ unit edges; this keeps distances but grows the graph.

## Applications

- **Flows and cuts.** Approximate maximum flow and minimum-cost flow algorithms in the multiplicative weights framework repeatedly route along short paths and then lengthen the used edges. This is a decremental shortest paths problem with an adaptive adversary, and the deterministic algorithms of 2021 were made for this use.
- **All-pairs structures.** Decremental all-pairs shortest paths and the fully dynamic algorithms built on it use Even-Shiloach trees from many sources.
- **Network failures.** Follow distances as links fail, with no repairs.

## References
