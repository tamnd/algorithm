---
tag: D7KE8A
kind: problem
slug: single-source-shortest-paths
name: Single-source shortest paths
aliases:
- SSSP
- single-source shortest path problem
area: graphs/shortest-paths
level: core
summary: Given a source s, compute shortest-path distances from s to all vertices.
prereqs: [shortest-path, negative-cycle, shortest-path-tree, edge-relaxation]
see_also: [dijkstra, bellman-ford, dag-shortest-paths, breadth-first-search, single-pair-shortest-path, all-pairs-shortest-paths, sorting-barrier, negative-cycle-detection]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, Single-Source Shortest Paths (introduction for the problem and its variants, Sections 22.1 to 22.3 for Bellman-Ford, DAGs and Dijkstra, and the chapter notes for the history of the bounds)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 596 to 615 (1987)
    locator: the section on shortest paths (Dijkstra in O(m + n log n))
  - paper: doi:10.1145/316542.316548
    title: Mikkel Thorup, Undirected single-source shortest paths with positive integer weights in linear time, Journal of the ACM 46(3), 362 to 394 (1999)
    locator: the main theorem
  - url: "https://arxiv.org/abs/2504.17033"
    locator: Ran Duan, Jiayi Mao, Xiao Mao, Xinkai Shu and Longhui Yin, Breaking the Sorting Barrier for Directed Single-Source Shortest Paths, STOC 2025 (the main theorem, O(m log^(2/3) n) in the comparison-addition model)
  - url: "https://arxiv.org/abs/2203.03456"
    locator: Aaron Bernstein, Danupon Nanongkai and Christian Wulff-Nilsen, Negative-Weight Single-Source Shortest Paths in Near-linear Time, FOCS 2022 (Theorem 1.1)
---

The single-source shortest paths problem (SSSP) asks for the [distance](/shortest-path/) $\delta(s, v)$ from one source vertex $s$ to every vertex $v$ of a weighted directed graph, together with a [shortest-path tree](/shortest-path-tree/) that gives one shortest path to each vertex. It is the central problem of this area: the [single-pair](/single-pair-shortest-path/) problem is solved through it, and the [all-pairs](/all-pairs-shortest-paths/) problem is often solved by $n$ runs of it. Which algorithm is best depends on the weights: [BFS](/breadth-first-search/) for unit weights, [Dijkstra's algorithm](/dijkstra/) in $O(m + n \log n)$ for nonnegative weights, and [Bellman-Ford](/bellman-ford/) in $O(nm)$ for negative weights, which must also detect [negative cycles](/negative-cycle/).

## In plain words

From one starting place, you want the cost of the cheapest route to every other place, and the routes themselves. The answer is a table with one number per place, and a "came from" mark per place that lets you rebuild each route.

All the usual methods start with the cost zero at the start and "unknown, so far infinite" everywhere else. They then look at roads one at a time: if going to the start of a road and then along it is cheaper than the best cost known at its end, they lower that cost. The methods differ in the order in which they look at the roads. A good order, such as "always continue from the closest place not yet done", needs to look at each road only once, but it works only when no road has a negative cost.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, a weight function $w : E \to \mathbb{R}$, and a source $s \in V$.

**Output.** For each $v \in V$ the value $\delta(s, v) \in \mathbb{R} \cup \{-\infty, +\infty\}$, and, when no [negative cycle](/negative-cycle/) is reachable from $s$, a parent $\pi(v)$ for each reachable $v \ne s$ such that the arcs $(\pi(v), v)$ form a [shortest-path tree](/shortest-path-tree/) rooted at $s$.

Many algorithms instead output either the finite distances and the tree, or the report "a negative cycle is reachable from $s$", with the cycle. Both forms are common; the second is what CLRS's BELLMAN-FORD returns. From the second form one gets the first in $O(n + m)$ extra time: the vertices with $\delta = -\infty$ are exactly those reachable from a vertex whose label can still be lowered after $n - 1$ rounds of Bellman-Ford.

**Weight assumptions.** Each algorithm assumes one of these, and its page states which:

- *unit weights*, $w \equiv 1$;
- *nonnegative weights*, $w(e) \ge 0$, real or integer;
- *integer weights*, $w(e) \in \mathbb{Z}$, often bounded: $0 \le w(e) \le C$, or $w(e) \ge -W$;
- *arbitrary real weights with no negative cycle reachable from $s$*, or with a report when one is reachable;
- *an acyclic graph*, with any real weights.

## Variants

- **Single destination.** Distances from every vertex to one target $t$: run SSSP from $t$ in the [transpose graph](/transpose-graph/).
- **Undirected graphs.** With nonnegative weights, replace each edge by two arcs. Negative undirected edges are a different problem (see [shortest path](/shortest-path/)).
- **DAGs.** Relax the arcs in [topological order](/topological-sort/): [DAG shortest paths](/dag-shortest-paths/), $O(n + m)$, any weights.
- **Weights 0 and 1, small integers.** [0-1 BFS](/zero-one-bfs/), [Dial's algorithm](/dial-algorithm/), [radix heaps](/radix-heap/).
- **Bottleneck objective.** Maximize the least weight on the path: the [widest path](/widest-path/) problem, solved by a Dijkstra with max and min in place of min and plus.
- **Time-dependent weights.** [Time-dependent shortest paths](/time-dependent-shortest-paths/).
- **Approximate.** Distances within a factor $1 + \varepsilon$, which matters in parallel and distributed models.

## Examples

**Negative arcs.** In the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7):

| $v$ | $s$ | $t$ | $x$ | $y$ | $z$ |
|---|---|---|---|---|---|
| $\delta(s, v)$ | 0 | 2 | 4 | 7 | $-2$ |
| $\pi(v)$ | nil | $x$ | $y$ | $s$ | $t$ |

**Nonnegative arcs.** In the graph of CLRS Figure 22.6, with the arcs $s \to t$ (10), $s \to y$ (5), $t \to x$ (1), $t \to y$ (2), $x \to z$ (4), $y \to t$ (3), $y \to x$ (9), $y \to z$ (2), $z \to s$ (7) and $z \to x$ (6):

| $v$ | $s$ | $t$ | $x$ | $y$ | $z$ |
|---|---|---|---|---|---|
| $\delta(s, v)$ | 0 | 8 | 9 | 5 | 7 |
| $\pi(v)$ | nil | $y$ | $t$ | $s$ | $y$ |

**A reachable negative cycle.** In the first graph with $x \to t$ set to $-6$, the cycle $t \to x \to t$ has weight $-1$ and every vertex is reachable from it, so $\delta(s, v) = -\infty$ for all five vertices.

**An unreachable vertex.** Add a vertex $u$ with the single arc $u \to s$. Then $\delta(s, u) = +\infty$ and $\pi(u) = \mathrm{nil}$; the rest of the answer does not change.

## Known algorithms

| algorithm | weights | time | model |
|---|---|---|---|
| [BFS](/breadth-first-search/) | all 1 | $O(n + m)$ | word RAM |
| [0-1 BFS](/zero-one-bfs/) | 0 or 1 | $O(n + m)$ | word RAM |
| [DAG shortest paths](/dag-shortest-paths/) | any, acyclic graph | $O(n + m)$ | comparison-addition |
| [Dijkstra](/dijkstra/), [binary heap](/binary-heap/) | $\ge 0$ | $O((n + m) \log n)$ | comparison-addition |
| [Dijkstra](/dijkstra/), [Fibonacci heap](/fibonacci-heap/) | $\ge 0$ | $O(m + n \log n)$ | comparison-addition |
| [Dial](/dial-algorithm/) | integers in $[0, C]$ | $O(m + nC)$ | word RAM |
| [Thorup](/thorup-undirected-sssp/) | positive integers, undirected | $O(m)$ | word RAM |
| [Duan, Mao, Mao, Shu and Yin](/breaking-sorting-barrier-sssp/) | $\ge 0$, directed | $O(m \log^{2/3} n)$ | comparison-addition |
| [Bellman-Ford](/bellman-ford/) | any, reports negative cycles | $O(nm)$ | comparison-addition |
| [SPFA](/spfa/) | any, reports negative cycles | $O(nm)$ worst case | comparison-addition |
| [Goldberg scaling](/goldberg-scaling-sssp/) | integers $\ge -W$ | $O(\sqrt{n}\, m \log W)$ | word RAM |
| [Near-linear negative SSSP](/near-linear-negative-sssp/) | integers $\ge -W$ | $O(m \log^8 n \log W)$ expected | word RAM |

## Bounds

**Nonnegative weights, comparison-addition model.** In this model the algorithm may add weights and compare sums, and nothing else. Dijkstra with a Fibonacci heap (Fredman and Tarjan 1987) takes $O(m + n \log n)$. For many years this was believed best, because Dijkstra finishes the vertices in sorted order of distance, and sorting $n$ numbers needs $\Omega(n \log n)$ comparisons; see the [sorting barrier](/sorting-barrier/). Duan, Mao, Mao, Shu and Yin (STOC 2025) broke it for directed graphs with a deterministic $O(m \log^{2/3} n)$ algorithm, which is faster when $m = o(n \log^{1/3} n)$. Their algorithm does not output the vertices in sorted order.

**Integer weights, word RAM.** Thorup (1999) solved the undirected case with positive integer weights in $O(m)$ time, which is optimal. For directed graphs, integer priority queues give $O(m + n \log \log n)$ (Thorup 2004).

**Negative weights.** For real weights, Bellman-Ford takes $O(nm)$; Fineman (STOC 2024) gave the first strongly polynomial improvement, randomized $\tilde O(m n^{8/9})$. For integer weights at least $-W$, Goldberg (1995) took $O(\sqrt{n}\, m \log W)$, and Bernstein, Nanongkai and Wulff-Nilsen (FOCS 2022) took $O(m \log^8 n \log W)$ expected, with later improvements to the logarithmic factors.

**Lower bound.** Each algorithm reads $\Omega(n + m)$ of the input in the worst case: it must look at each arc out of a reachable vertex, since an unread arc could be a shortcut. So BFS, 0-1 BFS, DAG shortest paths and Thorup's algorithm are optimal up to a constant factor. For an algorithm that must also output the vertices in order of distance, $\Omega(n \log n)$ comparisons are needed in the comparison model.

## Reductions

- **Single-pair to SSSP**, for free: read one entry.
- **APSP to SSSP**: $n$ runs, one from each source. With negative weights, [Johnson's algorithm](/johnson/) first computes a potential with one Bellman-Ford run, then runs Dijkstra $n$ times on nonnegative [reduced costs](/potential-function-reduced-costs/).
- **Negative weights to nonnegative weights.** Given a potential $h$ with $w(u, v) + h(u) - h(v) \ge 0$, SSSP on the reduced weights gives the same shortest paths. Finding $h$ is itself an SSSP problem with negative weights from an added source.
- **Negative cycle detection to SSSP.** Add a source $q$ with arcs of weight 0 to all vertices, and run an SSSP algorithm that reports negative cycles from $q$; see [negative cycle detection](/negative-cycle-detection/).
- **Difference constraints.** A system of constraints $x_j - x_i \le b_{ij}$ is feasible if and only if its constraint graph has no negative cycle, and the distances from the added source are a solution; see [difference constraints](/difference-constraints/).
- **Longest paths in a DAG.** Negate all weights; see [reduction of longest paths to shortest paths](/longest-to-shortest-paths-reduction/).

## Applications

- Route planning, network routing (OSPF computes a shortest-path tree at each router), and the routing of wires.
- Scheduling with precedence constraints, through [PERT charts](/pert-chart/) and difference constraints.
- Inner steps of other algorithms: [min-cost flow](/min-cost-flow-problem/) by successive shortest paths, [Johnson's algorithm](/johnson/), and [Yen's algorithm](/yen-k-shortest-paths/).
- Dynamic programs that are shortest paths in a DAG of states, such as edit distance and the sequence alignment problems.

## References
