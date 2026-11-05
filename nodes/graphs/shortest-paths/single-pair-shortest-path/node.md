---
tag: N918YN
kind: problem
slug: single-pair-shortest-path
name: Single-pair shortest path
aliases:
- point-to-point shortest path
- s-t shortest path
area: graphs/shortest-paths
level: intro
summary: Given s and t, compute the shortest s-t path.
prereqs: [shortest-path, weighted-graph, negative-cycle]
see_also: [single-source-shortest-paths, dijkstra, bidirectional-dijkstra, a-star-search, alt-algorithm, contraction-hierarchies, hub-labeling, k-shortest-paths]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction (the variants of the shortest-paths problem, and the remark that no single-pair algorithm is known to be asymptotically faster in the worst case than the best single-source algorithms)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths (the opening discussion of single-pair and single-source problems)
  - url: "https://arxiv.org/abs/1504.05140"
    locator: Hannah Bast, Daniel Delling, Andrew Goldberg, Matthias Müller-Hannemann, Thomas Pajor, Peter Sanders, Dorothea Wagner and Renato Werneck, Route Planning in Transportation Networks (2016), Section 2, Shortest paths algorithms (bidirectional search, goal-directed techniques, separators, hierarchical techniques, bounded-hop techniques)
---

The single-pair shortest path problem asks for a [shortest path](/shortest-path/) from one given vertex $s$ to one given vertex $t$ of a weighted directed graph, or a report that none exists. It looks easier than the [single-source](/single-source-shortest-paths/) problem, but no algorithm is known that is faster in the worst case: the standard method is [Dijkstra's algorithm](/dijkstra/) from $s$, stopped when $t$ is finished. In practice it is the most asked shortest-path question, because route planners answer it millions of times on the same road network, and preprocessing such as [contraction hierarchies](/contraction-hierarchies/) and [hub labels](/hub-labeling/) makes each query take microseconds.

## In plain words

You want the best route from one place to one other place, not to all places. Each road has a cost, such as its length or its travel time. The best route is the one with the least total cost.

The usual method grows a region around the start, always adding the closest place that is not yet in the region. When the goal enters the region, its best route is known and the search can stop. To go faster, one can search from both ends at once, or guide the search toward the goal, or prepare extra data about the map in advance so that each question needs only a small search.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, weights $w : E \to \mathbb{R}$, and two vertices $s, t \in V$.

**Output.** One of three answers.

- $t$ is not reachable from $s$: $\delta(s, t) = +\infty$.
- Some walk from $s$ to $t$ meets a [negative cycle](/negative-cycle/): $\delta(s, t) = -\infty$.
- Otherwise, the value $\delta(s, t)$ and a path $p$ from $s$ to $t$ with $w(p) = \delta(s, t)$, which can be taken simple.

**Weight assumptions.** Each algorithm below states which case it handles: nonnegative weights ($w \ge 0$), integer weights (often $0 \le w \le C$), or arbitrary real weights with no negative cycle in reach.

## Variants

- **Unweighted.** All weights are 1. [Breadth-first search](/breadth-first-search/) from $s$ solves it in $O(n + m)$.
- **Weights 0 and 1.** [0-1 BFS](/zero-one-bfs/) solves it in $O(n + m)$.
- **Nonnegative weights.** Dijkstra from $s$, stopped when $t$ leaves the queue.
- **Negative weights.** No early stop is safe: an arc found late can still lower $\delta(s, t)$. Solve the single-source problem with [Bellman-Ford](/bellman-ford/).
- **DAG.** Relax the arcs in [topological order](/dag-shortest-paths/), in $O(n + m)$, with any weights.
- **Many queries on one graph.** Preprocess the graph, then answer each pair fast. This is the [distance oracle](/distance-oracle/) setting; exact versions are [contraction hierarchies](/contraction-hierarchies/), [highway hierarchies](/highway-hierarchies/) and [hub labeling](/hub-labeling/), and approximate ones include the [Thorup-Zwick oracle](/thorup-zwick-oracle/).
- **Several answers.** The $k$ best paths, in the [k shortest paths](/k-shortest-paths/) problem.
- **Side constraints.** A budget on a second weight, in the [constrained shortest path](/constrained-shortest-path/) problem, which is NP-hard.
- **Time-dependent weights.** [Time-dependent shortest paths](/time-dependent-shortest-paths/).

## Examples

**Negative arcs.** In the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), the answer for the pair $(s, z)$ is $\delta(s, z) = -2$ with the path $s \to y \to x \to t \to z$. The direct-looking path $s \to t \to z$ has weight 2.

**Early stop with nonnegative weights.** In the graph of CLRS Figure 22.6, with the arcs $s \to t$ (10), $s \to y$ (5), $t \to x$ (1), $t \to y$ (2), $x \to z$ (4), $y \to t$ (3), $y \to x$ (9), $y \to z$ (2), $z \to s$ (7) and $z \to x$ (6), Dijkstra from $s$ finishes the vertices in the order $s$ (0), $y$ (5), $z$ (7), $t$ (8), $x$ (9). For the pair $(s, z)$ it can stop after three of the five vertices, with $\delta(s, z) = 7$ by the path $s \to y \to z$. For the pair $(s, x)$ it finishes all five, with $\delta(s, x) = 9$ by $s \to y \to t \to x$.

**Why the early stop fails with a negative arc.** Take $s \to t$ (2), $s \to a$ (3) and $a \to t$ ($-2$). Dijkstra finishes $t$ first with the value 2, but $\delta(s, t) = 1$ by $s \to a \to t$.

**Unreachable.** If $t$ has no incoming arc and $t \ne s$, the answer is $+\infty$ and there is no path.

**Negative cycle.** In the first graph, with $x \to t$ changed to $-6$, the cycle $t \to x \to t$ has weight $-1$ and reaches $z$, so $\delta(s, z) = -\infty$.

## Known algorithms

| algorithm | weights | time per query | preprocessing |
|---|---|---|---|
| [BFS](/breadth-first-search/) | all 1 | $O(n + m)$ | none |
| [0-1 BFS](/zero-one-bfs/) | 0 or 1 | $O(n + m)$ | none |
| [Dijkstra](/dijkstra/) with a [Fibonacci heap](/fibonacci-heap/), early stop | $\ge 0$ | $O(m + n \log n)$ | none |
| [Dial's algorithm](/dial-algorithm/) | integers in $[0, C]$ | $O(m + nC)$ | none |
| [Bidirectional Dijkstra](/bidirectional-dijkstra/) | $\ge 0$ | same worst case, often far less | none |
| [A* search](/a-star-search/), [ALT](/alt-algorithm/) | $\ge 0$, consistent bounds | same worst case, goal-directed | ALT: distances to landmarks |
| [Contraction hierarchies](/contraction-hierarchies/) | $\ge 0$ | small on road networks, no good worst case | contraction order and shortcuts |
| [Hub labeling](/hub-labeling/) | $\ge 0$ | $O(\lvert L(s) \rvert + \lvert L(t) \rvert)$ | the labels |
| [DAG shortest paths](/dag-shortest-paths/) | any, acyclic graph | $O(n + m)$ | none |
| [Bellman-Ford](/bellman-ford/) | any, reports negative cycles | $O(nm)$ | none |

## Bounds

**Upper bound.** The single-pair problem reduces to the single-source problem, so every bound of [single-source shortest paths](/single-source-shortest-paths/) applies: $O(m + n \log n)$ for nonnegative real weights in the comparison-addition model, $O(m)$ for undirected graphs with positive integer weights on the word RAM ([Thorup](/thorup-undirected-sssp/)), and $O(nm)$ for real weights with negative arcs.

**No known gap.** CLRS (Chapter 22, introduction) notes that no single-pair algorithm is known that runs asymptotically faster in the worst case than the best single-source algorithms. An early stop helps only when $t$ is close to $s$.

**Lower bound.** In the worst case an algorithm must read $\Omega(m)$ arcs: an arc whose weight it has not read could have weight 0 and create a shorter path to $t$. So $\Omega(n + m)$ time is needed without preprocessing. With preprocessing, exact labels for general graphs need $\Omega(n)$ bits per vertex for some graphs (Gavoille, Peleg, Pérennes and Raz), so a fast query with small space is only possible for special graph classes.

## Reductions

- **To single-source.** Run a single-source algorithm from $s$ and read $\delta(s, t)$. Cost: one single-source run.
- **Reverse graph.** The pair $(s, t)$ in $G$ is the pair $(t, s)$ in the [transpose graph](/transpose-graph/). Bidirectional search uses both.
- **Undirected to directed.** With nonnegative weights, replace each edge by two arcs.

## Applications

- Route planning in road and transit networks, with preprocessing.
- Routing of packets and wires in networks and chips.
- Path finding for agents in games, often with A*.
- Inner steps of other algorithms: augmenting paths in min-cost flow, spur paths in [Yen's algorithm](/yen-k-shortest-paths/), and the alignment of sequences as a shortest path in a grid DAG.

## References
