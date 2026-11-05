---
tag: V4JHJM
kind: problem
slug: widest-path
name: Widest path
aliases:
- maximum-capacity path
- bottleneck path
- maximin path
area: graphs/shortest-paths
level: core
summary: Find an s-t path maximizing the minimum edge capacity along it.
prereqs: [shortest-path, dijkstra, maximum-spanning-tree]
see_also: [dijkstra, maximum-spanning-tree, minimum-bottleneck-spanning-tree, kruskal, floyd-warshall, max-flow-problem, edmonds-karp, capacity-scaling]
sources:
  - paper: "Maurice Pollack, The maximum capacity through a network, Operations Research 8(5), 733 to 736 (1960)"
    locator: the definition of the problem and the labeling method
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths (the exercise on maximum-bandwidth paths) and Chapter 7, Minimum Spanning Trees
  - paper: "Harold N. Gabow and Robert E. Tarjan, Algorithms for two bottleneck optimization problems, Journal of Algorithms 9(3), 411 to 417 (1988)"
    locator: the bottleneck path from s to t in a directed graph in O(m log* n) time
  - paper: "Paolo M. Camerini, The min-max spanning tree problem and some extensions, Information Processing Letters 7(1), 10 to 14 (1978)"
    locator: the linear-time minimum bottleneck spanning tree, which gives undirected bottleneck paths
  - paper: "Ran Duan and Seth Pettie, Fast algorithms for (max, min)-matrix multiplication and bottleneck shortest paths, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2009, 384 to 391"
    locator: all-pairs bottleneck paths in O(n^((3+ω)/2)) time
  - url: https://en.wikipedia.org/wiki/Widest_path_problem
    title: Wikipedia, Widest path problem
    locator: sections Undirected graphs, Directed graphs and Applications (the Schulze method and max-flow augmenting paths)
---

The widest path problem asks for a path from $s$ to $t$ whose smallest arc capacity is as large as possible. This smallest capacity is the *width* or *bottleneck* of the path. It is a shortest-path problem with the sum of weights replaced by their minimum and the minimum over paths replaced by a maximum. [Dijkstra's algorithm](/dijkstra/) solves it with the same changes, and in an undirected graph every path in a [maximum spanning tree](/maximum-spanning-tree/) is a widest path. Cycles never help a widest path, so negative or arbitrary capacities cause no trouble.

## In plain words

Each road has a limit, for example the heaviest truck it can carry. A route can carry only what its weakest road carries. The widest path problem asks for the route from one place to another that can carry the most.

The cheapest-route methods still work with two changes: a route is as good as its weakest road, not the sum of its roads, and you want the largest such value, not the smallest. Going around a loop can never make a route stronger, because each extra road can only lower the weakest limit.

## Definition

Let $G = (V, E)$ be a directed or undirected graph with capacities $c : E \to \mathbb{R}$, and let $s, t \in V$. The *width* of a path $p = \langle v_0, \ldots, v_k \rangle$ with $k \ge 1$ is

$$b(p) = \min_{1 \le i \le k} c(v_{i-1}, v_i),$$

and the empty path $\langle s \rangle$ has width $+\infty$. The *widest-path value* is

$$\beta(s, t) = \max \{ b(p) : p \text{ is a path from } s \text{ to } t \},$$

with $\beta(s, t) = -\infty$ if no path exists. A widest path is a path with $b(p) = \beta(s, t)$. The single-source problem asks for $\beta(s, v)$ for all $v$, and the all-pairs problem asks for all pairs.

**Weight assumptions.** Capacities may be any real numbers, negative ones included, because only comparisons are used. There is no analogue of a negative cycle: a walk that repeats a vertex has width at most that of the path left after removing the cycle, so walks and paths give the same value. Unreachable targets have the value $-\infty$. Integer capacities are only needed for the faster algorithms that use radix sorting or bit tricks.

## Variants

- **Single pair, single source, all pairs.** As for shortest paths. In undirected graphs, one maximum spanning tree answers all pairs.
- **Minimax or bottleneck shortest path.** Minimize the largest weight on the path. It is the same problem with $c$ replaced by $-c$.
- **Widest shortest path.** Among the shortest paths by length, find one of largest width, or among the widest paths find one of least length. Both are solved by Dijkstra with pairs of labels compared in lexicographic order.
- **Directed or undirected.** The undirected problem has more structure: it reduces to spanning trees and has linear-time algorithms for one pair.
- **Most reliable path.** Maximize the product of probabilities. It is not a widest path problem; it becomes a shortest path problem under $-\log$.

## Examples

**Directed, from one source.** Take the arcs $s \to t$ (10), $s \to y$ (5), $t \to x$ (1), $t \to y$ (2), $x \to z$ (4), $y \to t$ (3), $y \to x$ (9), $y \to z$ (2), $z \to s$ (7) and $z \to x$ (6) as capacities. The widest values from $s$ are:

| $v$ | $\beta(s, v)$ | a widest path |
|---|---|---|
| $s$ | $+\infty$ | $\langle s \rangle$ |
| $t$ | 10 | $s \to t$ |
| $y$ | 5 | $s \to y$ |
| $x$ | 5 | $s \to y \to x$ |
| $z$ | 4 | $s \to y \to x \to z$ |

The shortest path from $s$ to $x$ under the same numbers as lengths is $s \to y \to t \to x$ of length 9, but its width is 1. Widest and shortest paths are different in general.

**Modified Dijkstra.** Keep labels $B(v)$, start with $B(s) = +\infty$ and $B(v) = -\infty$ otherwise, take the vertex of largest label each time, and relax an arc by $B(v) \leftarrow \max(B(v), \min(B(u), c(u, v)))$. On the example, the vertices finish in the order $s$ ($+\infty$), $t$ (10), $y$ (5), $x$ (5), $z$ (4). The proof is the proof of Dijkstra with $(\max, \min)$ in place of $(\min, +)$: extending a path never raises its width, which plays the role of nonnegative weights.

**Undirected, by a maximum spanning tree.** Take the edges $a$-$b$ (4), $b$-$c$ (2), $a$-$c$ (3), $c$-$d$ (5) and $b$-$d$ (1). A maximum spanning tree is $\{c\text{-}d, a\text{-}b, a\text{-}c\}$. The tree path from $b$ to $d$ is $b, a, c, d$ with width $\min(4, 3, 5) = 3$, and indeed the other routes $b$-$d$ (1) and $b$-$c$-$d$ (2) are narrower.

**Negative capacities and cycles.** With capacities $s \to a$ ($-3$), $a \to b$ ($-1$), $b \to a$ ($-1$), the value $\beta(s, b) = -3$, and going around the cycle $a \to b \to a$ gives walks of width $-3$ again, never more. No special case is needed.

**Unreachable.** If $t$ has no arc into it, $\beta(s, t) = -\infty$ and every algorithm leaves its label at $-\infty$.

## Known algorithms

| algorithm | graph | output | time |
|---|---|---|---|
| modified [Dijkstra](/dijkstra/) with a Fibonacci heap | directed | single source | $O(m + n \log n)$ |
| sort the capacities, then binary search on a threshold with one BFS per step | directed or undirected | single pair | $O(m \log n)$ |
| [Kruskal](/kruskal/) for a [maximum spanning tree](/maximum-spanning-tree/), then tree paths | undirected | all pairs | $O(m \log n + n^2)$ |
| [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/) style median splitting (Camerini) | undirected | single pair | $O(m)$ |
| Gabow and Tarjan | directed | single pair | $O(m \log^* n)$ |
| [Floyd-Warshall](/floyd-warshall/) over $(\max, \min)$ | directed | all pairs | $\Theta(n^3)$ |
| Duan and Pettie, $(\max, \min)$ matrix product | directed | all pairs | $O(n^{(3 + \omega)/2})$, about $O(n^{2.69})$ |

The single-pair bounds use the fact that only the order of the capacities matters: the answer is the largest capacity $c^*$ such that $t$ is reachable from $s$ using only arcs of capacity at least $c^*$. Median finding lets one halve the candidate capacities in linear time per step.

## Bounds

- **Lower bound.** Any algorithm must look at $\Omega(m)$ arcs in the worst case for one pair, so the undirected $O(m)$ bound is optimal.
- **Directed graphs.** Only the order of the capacities matters, so the problem does not need a priority queue of real keys. For one pair, Gabow and Tarjan get $O(m \log^* n)$ in the comparison model, below the $O(m + n \log n)$ of Dijkstra on sparse graphs. Whether a directed single pair can be solved in $O(m)$ time is open.
- **All pairs.** The $(\max, \min)$ matrix product is truly subcubic, unlike the $(\min, +)$ product: $O(n^{(3 + \omega)/2})$, where $\omega < 2.372$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). So all-pairs widest paths is easier than [all-pairs shortest paths](/all-pairs-shortest-paths/) under the APSP conjecture.

## Reductions

- **To reachability with a threshold.** For a value $c^*$, keep the arcs with capacity at least $c^*$; then $\beta(s, t) \ge c^*$ if and only if $t$ is reachable from $s$. A binary search over the sorted capacities gives $\beta(s, t)$ with $O(\log m)$ searches.
- **To spanning trees (undirected).** For every pair, the path in a maximum spanning tree is a widest path. This follows from the cut property: if the tree path had an edge narrower than some path outside the tree, exchanging edges would give a heavier spanning tree.
- **To the algebraic path problem.** Widest paths are shortest paths over the semiring $(\mathbb{R} \cup \{\pm\infty\}, \max, \min)$; any algorithm for closed semirings, such as Floyd-Warshall or repeated squaring, applies.
- **From minimax paths.** Negate the weights.

## Applications

- **Maximum flow.** The augmenting path of largest residual capacity, the "fattest path", gives a max-flow algorithm with $O(m \log U)$ augmentations for integer capacities at most $U$; it is a widest path in the residual graph. See [Edmonds-Karp](/edmonds-karp/) and [capacity scaling](/capacity-scaling/).
- **Network routing.** The route with the largest bandwidth, where the bandwidth of a route is that of its slowest link.
- **The Schulze voting method.** The strength of a chain of pairwise preferences is its weakest link, and the winner is found from all-pairs widest paths by a Floyd-Warshall variant.
- **Image processing.** The connectedness of two pixels as the largest, over paths, of the smallest similarity along the path; this is used in fuzzy connectedness segmentation.
- **Mountain passes and flooding.** In a terrain, the lowest pass between two valleys is a minimax path, and the minimax values describe when two basins merge as water rises.

## References
