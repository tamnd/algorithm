---
tag: BKBYDH
kind: problem
slug: dynamic-single-source-shortest-paths
name: Dynamic single-source shortest paths
aliases:
- dynamic SSSP
area: graphs/dynamic-graphs
level: advanced
summary: Maintain shortest-path distances from a fixed source under edge updates.
prereqs: [dynamic-graph, single-source-shortest-paths, dijkstra, decremental-graph]
see_also: [decremental-sssp, even-shiloach-tree, ramalingam-reps, dynamic-all-pairs-shortest-paths, dynamic-reachability, bellman-ford, negative-cycle]
sources:
  - paper: doi:10.1006/jagm.1996.0046
    title: G. Ramalingam and Thomas Reps, An incremental algorithm for a generalization of the shortest-path problem, Journal of Algorithms 21(2), 267 to 305 (1996)
    locator: the whole paper (bounded update time in terms of the changed part of the output)
  - paper: doi:10.1006/jagm.1999.1048
    title: Daniele Frigioni, Alberto Marchetti-Spaccamela and Umberto Nanni, Fully dynamic algorithms for maintaining shortest paths trees, Journal of Algorithms 34(2), 251 to 281 (2000)
    locator: the whole paper (output-bounded fully dynamic algorithms for a shortest paths tree)
  - paper: doi:10.1145/322234.322235
    title: Shimon Even and Yossi Shiloach, An on-line edge-deletion problem, Journal of the ACM 28(1), 1 to 4 (1981)
    locator: the breadth-first tree with levels that only grow (O(mn) total time under deletions)
  - paper: doi:10.1007/s00453-010-9401-5
    title: Liam Roditty and Uri Zwick, On dynamic shortest paths problems, Algorithmica 61(2), 389 to 401 (2011)
    locator: the reductions from static all-pairs shortest paths and Boolean matrix multiplication to incremental and decremental single-source shortest paths
---

The dynamic single-source shortest paths problem asks to keep the distances $d(s, v)$ from a fixed source $s$ to every vertex of a weighted [dynamic graph](/dynamic-graph/) while edges are inserted, deleted or change weight. The static problem is [single-source shortest paths](/single-source-shortest-paths/), solved by [Dijkstra's algorithm](/dijkstra/) in $O(m + n \log n)$ time for nonnegative weights, so recomputation after each update is the baseline. Updates that only shorten paths are easy to propagate. Updates that only lengthen paths are harder, and for the exact problem with both kinds, no general algorithm is known that is much faster than recomputation in the worst case.

## In plain words

A delivery company keeps, for each town, the shortest driving time from its depot. Roads open, close, get faster or get slower.

When a road gets faster, only towns whose best route can now use that road improve, and the company can spread the news from that road outward, like a search that starts there. When a road gets slower or closes, every town whose best route used it must look for a new best route, and the new routes may be much longer or not exist. The work is small when few towns change, but one closed road can change the times of almost every town.

## Definition

**Input.** A directed graph $G = (V, E)$ on $n$ vertices with edge weights $w : E \to \mathbb{R}_{\ge 0}$, a source $s \in V$, and an online sequence of updates:

- $\mathrm{insert}(u, v, x)$ adds the edge $(u, v)$ with weight $x$,
- $\mathrm{delete}(u, v)$ removes the edge $(u, v)$,
- $\mathrm{setweight}(u, v, x)$ changes the weight of $(u, v)$ to $x$,

mixed with queries $\mathrm{dist}(v)$, which return $d(s, v)$, the weight of a lightest directed path from $s$ to $v$, or $\infty$ if there is none. A stronger form also returns the path, or keeps a shortest-path tree rooted at $s$.

**Kinds of update.** An insertion or a weight decrease can only lower distances: this is the **incremental** problem. A deletion or a weight increase can only raise them: this is the **decremental** problem. With both, the problem is **fully dynamic**. Each bound is worst case, [amortized](/amortized-update-time/) or expected.

**Negative weights.** With negative weights and no negative cycle, distances are still defined, but a weight decrease can create a [negative cycle](/negative-cycle/), and the structure must report it.

## Variants

- **Incremental.** Insertions and weight decreases.
- **Decremental.** Deletions and weight increases; see [decremental SSSP](/decremental-sssp/).
- **Fully dynamic.** All updates.
- **Unweighted.** Distances are numbers of edges, so each distance is an integer from $0$ to $n - 1$ or $\infty$.
- **Approximate.** Keep estimates $\tilde d(v)$ with $d(s, v) \le \tilde d(v) \le (1 + \varepsilon)\, d(s, v)$. Most fast decremental algorithms are of this kind.
- **Single pair.** Keep only $d(s, t)$ for fixed $s$ and $t$.
- **All pairs.** Keep all distances; see [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/).

## Examples

Take $V = \{0, \ldots, 4\}$, source $0$, and the edges $0 \to 1$ (4), $0 \to 2$ (1), $2 \to 1$ (2), $1 \to 3$ (5), $2 \to 3$ (8), $3 \to 4$ (3), with weights in brackets. The distances $(d(0), \ldots, d(4))$ start at $(0, 3, 1, 8, 11)$.

| update | distances after it | changed vertices |
|---|---|---|
| set weight of $2 \to 3$ to 2 | 0, 3, 1, 3, 6 | 3, 4 |
| insert $0 \to 4$ (4) | 0, 3, 1, 3, 4 | 4 |
| delete $0 \to 2$ | 0, 4, ∞, 9, 4 | 1, 2, 3 |
| set weight of $1 \to 3$ to 1 | 0, 4, ∞, 5, 4 | 3 |
| delete $0 \to 4$ | 0, 4, ∞, 5, 8 | 4 |
| insert $4 \to 2$ (1) | 0, 4, 9, 5, 8 | 2 |

The first two updates shorten paths, and only vertices downstream of the changed edge improve. The deletion of $0 \to 2$ removes the first edge of three shortest paths at once: vertex 2 becomes unreachable, and 1 and 3 fall back to longer routes. The last update makes 2 reachable again, through a path of four edges.

## Known algorithms

**Incremental propagation.** After an insertion or decrease of $(u, v)$, if $d(u) + w(u, v) < d(v)$, set $d(v)$ to this value and run Dijkstra's algorithm from $v$ with a priority queue that holds only the improved vertices. A vertex enters the queue only if its distance drops, so the work is $O(\|\delta\| \log \|\delta\|)$, where $\|\delta\|$ is the number of changed vertices plus their out-edges. This is deterministic and worst case per update, but it is a bound in the size of the change, not in $n$ and $m$.

**Bounded fully dynamic algorithms.** Ramalingam and Reps (1996) handle deletions and increases too. After an increase of $(u, v)$ they first find the affected vertices, whose every shortest path used the edge, and then recompute only their distances with a Dijkstra-like pass seeded from their unaffected in-neighbors. The cost is again $O(\|\delta\| \log \|\delta\|)$ per update, deterministic; see [Ramalingam and Reps](/ramalingam-reps/). Frigioni, Marchetti-Spaccamela and Nanni (2000) give related output-bounded algorithms. In the worst case $\|\delta\|$ is $\Theta(n + m)$, so these bounds do not beat recomputation for every sequence.

**Decremental, unweighted.** The [Even-Shiloach tree](/even-shiloach-tree/) keeps a breadth-first tree whose levels only grow, in $O(mn)$ total time over all deletions, which is $O(n)$ amortized per deletion, deterministic. With positive integer weights and distances at most $D$ that are tracked, the same idea costs $O(mD)$ total.

**Decremental, approximate.** Much faster algorithms keep $(1 + \varepsilon)$-approximate distances under deletions, with total time close to $m$ in undirected graphs; see [decremental SSSP](/decremental-sssp/).

| setting | method | time | case | deterministic |
|---|---|---|---|---|
| fully dynamic | recompute with Dijkstra | $O(m + n \log n)$ per update | worst | yes |
| fully dynamic | Ramalingam and Reps (1996) | $O(\|\delta\| \log \|\delta\|)$ per update | worst, output-bounded | yes |
| incremental, unweighted | propagation | $O(mn)$ total | amortized | yes |
| decremental, unweighted | Even-Shiloach tree | $O(mn)$ total | amortized | yes |

For the incremental unweighted row: each distance only drops, from at most $n - 1$ to $0$, and a drop of $v$ scans its out-edges, so the total is $O(mn)$.

## Bounds

**Upper bounds.** As in the table. For the exact fully dynamic problem on general weighted graphs, no algorithm is known with an update time polynomially smaller than $m$ in the worst case.

**Conditional lower bounds.** Roditty and Zwick (2004, journal 2011) show that the incremental and the decremental problems on weighted graphs are at least as hard as static [all-pairs shortest paths](/all-pairs-shortest-paths/): a structure with small update and query time would give an all-pairs algorithm much faster than the known ones. For unweighted graphs they give a similar reduction from Boolean matrix multiplication, which applies to combinatorial algorithms. So the $O(mn)$ total of the Even-Shiloach tree is hard to beat for exact distances.

## Reductions

- **Reachability.** $v$ is reachable from $s$ if and only if $d(s, v) < \infty$, so [dynamic reachability](/dynamic-reachability/) reduces to this problem.
- **Weight changes.** A weight change is a deletion followed by an insertion. In the other direction, a deletion is an increase to a large weight.
- **All pairs.** Running one structure per source gives dynamic all-pairs distances with $n$ times the cost.

## Applications

- **Routing.** Link-state routing protocols keep a shortest-path tree from each router and update it when link costs change, instead of a full recomputation.
- **Navigation.** Travel times change with traffic, and a route planner keeps distances from the current position.
- **Program analysis and incremental computation.** Ramalingam and Reps studied the problem as a case of keeping the result of a computation under small changes to its input.
- **Building block.** Decremental distance structures are parts of fast algorithms for flows and cuts.

## References
